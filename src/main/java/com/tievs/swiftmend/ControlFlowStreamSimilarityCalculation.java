package com.tievs.swiftmend;

import com.google.gson.Gson;
import com.tievs.swiftmend.utils.*;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.SQLOutput;
import java.time.Duration;
import java.time.Instant;
import java.util.*;


public class ControlFlowStreamSimilarityCalculation {
    private HashMap<String, HashMap<String, Integer>> activityIndices = new HashMap<>();
    private HashMap<String, Integer> activityToIndex = new HashMap<>();
    private HashMap<String, String> activityTimestamp = new HashMap<>();
    HashMap<String, String> lastActivityTimestamp = new HashMap<>();
    HashMap<String, Integer> activityCount = new HashMap<>();
    HashMap<String, Integer> lastActivityCount = new HashMap<>();
    private int activityIndexCounter = 0;
    private HashMap<String, int[]> caseActivityIndices = new HashMap<>();
    private HashMap<String, Integer>[][] directlyFollows = new HashMap[1][1];// Initialize with a default size
    HashMap<ActivityPair, Float> similarityMap = new HashMap<>();
    private int[][] footprintMatrix = new int[1][1];// Initialize with a default size

    private int[][] prevFootprint = new int[1][1];

    // Initialize the adjacency list
    Map<String, List<String>> mergeSet = new HashMap<>();

    Map<String, List<String>> previousMergeSet;
    private int cThreshold = 0;
    private double eventCounter = 0;
//    private final double windowSize = 451;
    private final double windowSize = Double.parseDouble(System.getProperty("window"));
//    private final int delay = 0;
    private final int delay = Integer.parseInt(System.getProperty("delay"));
//    final float controlFlowSimThreshold = 0.7F;
    final float controlFlowSimThreshold = Float.parseFloat(System.getProperty("simt"));
    private final String outputFile = System.getProperty("output");
//    private final String outputFilePath = "C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/HospitalB_EachEvent_451_0_0.7_test_modified.csv";
    private final String outputFilePath = "C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/HospitalB_EachEvent_"+outputFile+"_modified_onlyFIN_sections3.csv";
    // Define the upper and lower threshold
    //private final String outputFilePathforFootprint = "C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/"+outputFile+"_modifiedOnlyNew_prob_footprint.csv";
    final float upperCausalityThreshold = 0.8F; // upper threshold value
    final float upperParallelismThreshold = 2;
    final float lowerCausalityThreshold = 0.7F; // lower threshold value
    final float lowerParallelismThreshold = 3;


    private Duration totalProcessingTime = Duration.ZERO;

    private BufferedWriter eachEventWriter, forgetTriggeredWriter;
    Map<String, List<Pair<String, Float>>> adjacencyList = new HashMap<>();

    private Boolean clusteringHappen = false;
    IncrementalHierarchicalClustering clustering = new IncrementalHierarchicalClustering(adjacencyList, controlFlowSimThreshold);

    public ControlFlowStreamSimilarityCalculation() {
        // ...
        try {
            //forgetTriggeredWriter = new BufferedWriter(new FileWriter("C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/HospitalB_ForgetTriggered_1100_1_0.7_modified2.csv"));
            eachEventWriter = new BufferedWriter(new FileWriter(outputFilePath));
//          forgetTriggeredWriter = new BufferedWriter(new FileWriter("C:/Git/SwiftMend/Test1.csv"));
//          eachEventWriter = new BufferedWriter(new FileWriter("C:/Git/SwiftMend/Test2.csv"));
            //forgetTriggeredWriter.write("Event Counter,Input Activity,Output Activity,Activity Count,Merge Set\n");
            eachEventWriter.write("Event Counter,Input Activity,Output Activity,Activity Count,Merge Set\n");
        } catch (IOException e) {
            // System.out.println("Error occurred while opening the file: " + e.getMessage());
        }
    }
    public void processActivity(String caseId, String activity, String timestamp) {
        clusteringHappen = false;
        Instant start = Instant.now();
        // System.out.println();
        // System.out.println("=====================================================================================================================");
        // System.out.println();
        eventCounter++;
         System.out.println("Event Counter: " + eventCounter);
        activityTimestamp.put(activity, timestamp);
        // System.out.println(activityTimestamp.get(activity));
        // Add activity to activityIndices if it's not already present
        HashMap<String, Integer> activityData = activityIndices.get(activity);
        if (activityData == null) {
            activityData = new HashMap<>();
            activityData.put(caseId, 1);
            activityIndices.put(activity, activityData);
            activityToIndex.put(activity, activityIndexCounter++);
            activityCount.put(activity, 1);
        } else {
            activityData.put(caseId, activityData.getOrDefault(caseId, 0) + 1);
            activityCount.put(activity, activityCount.get(activity) + 1);
        }
        //print received caseId and activity in one line
        // System.out.println("New Event => caseID: " + caseId + ", activity: " + activity + ", activityIndex: " + activityToIndex.get(activity));

        // Resize directlyFollows if necessary
        if (activityIndices.size() > directlyFollows.length) {
            directlyFollows = resizeMatrix(directlyFollows, activityIndices.size());
            footprintMatrix = resizeFootprintMatrix(footprintMatrix, activityIndices.size());
        }


        int[] indices = caseActivityIndices.getOrDefault(caseId, new int[]{-1, -1, cThreshold-1});
        indices[0] = indices[1];
        indices[1] = activityToIndex.get(activity);
        indices[2]++; // Increment the activity count
        //print case details
        // System.out.println(caseId+" Case existing details: last activity: "+ getActivityFromIndex(indices[0]) + " caseIDCounter: "+ (indices[2] - 1));
        caseActivityIndices.put(caseId, indices);

        // Update directlyFollows matrix
        if (indices[0] != -1 && indices[1] != -1) {
            if (directlyFollows[indices[0]][indices[1]] == null) {
                directlyFollows[indices[0]][indices[1]] = new HashMap<>();
            }
            directlyFollows[indices[0]][indices[1]].put(caseId, directlyFollows[indices[0]][indices[1]].getOrDefault(caseId, 0) + 1);
        }
        // after updating directly follows matrix we need to check for footprint update check
        // Update the Footprint Method
        footprintUpdate(indices[0], indices[1]);
        //saveFootprintMatrixToCSV(outputFilePathforFootprint);

        //print all
        // System.out.println("distAct: " + activityIndices.toString());
        // System.out.println("Activity Count: " + activityCount);
        for (HashMap.Entry<String, int[]> entry : caseActivityIndices.entrySet()) {
            String key = entry.getKey();
            int[] value = entry.getValue();
            // System.out.println(key + " Case new details: last activity: " + getActivityFromIndex(value[1]) + ", caseIDCounter: " + value[2]);
        }

        // System.out.println();
        //activityToIndex.forEach((k, v) ->  System.out.println("Index of '" + k + "': " + v));
        // System.out.println();
        // System.out.println("directFollows: " + Arrays.deepToString(directlyFollows));;
        // System.out.println("Previous Footprint");
        //printFootprintMatrix(prevFootprint);
        // System.out.println("Current Footprint");
        //printFootprintMatrix(footprintMatrix);
        // System.out.println();

        int floorValue = (int) Math.floor(eventCounter / windowSize);
        // forgetting logic; eventCounter / windowSize floor value not equal to cThreshold
        if (floorValue != cThreshold) {

            // System.out.println();
            // System.out.println("*************************************************************************************");
            // System.out.println("Forgetting triggered, eventCounter/windowSize floor value: " + floorValue + ", caseIDCounter considered for caseID forgetting (cThreshold - delay): " + (cThreshold - delay));
            //save forgetCases in a set
            Set<UniquePair> forgetCases = forgetCases();
            // if forgetCases is not empty; loop through pair and call footprintUpdate
            if (!forgetCases.isEmpty()) {
                for (UniquePair pair : forgetCases) {
                    footprintUpdate(pair.getFirst(), pair.getSecond());
                }
            }
            cThreshold = floorValue;
            // System.out.println("New cThreshold: " + cThreshold);
            // ...
//            if (forgetTriggeredWriter != null) {
//                try {
//                    Map<String, String> activityCluster = clustering.getActivityToCluster();
//                    String outputActivity = activityCluster.get(activity);
//                    String outputActivityValue = (outputActivity != null) ? outputActivity : activity;
//                    forgetTriggeredWriter.write((eventCounter-1) + ",");
//                    forgetTriggeredWriter.write(activity + ",");
//                    forgetTriggeredWriter.write(outputActivityValue + ",");
//                    forgetTriggeredWriter.write(activityCount.toString() + ",");
//                    forgetTriggeredWriter.write(mergeSet + "\n");
//                    forgetTriggeredWriter.flush();
//                } catch (IOException e) {
//                    // System.out.println("Error occurred while writing to the file: " + e.getMessage());
//                }
//            }
        }
        if(!clusteringHappen){
            // Find the group in the mergeSet that contains the current 'activity'
            String groupWithCurrentActivity = null;
            for (Map.Entry<String, List<String>> entry : mergeSet.entrySet()) {
                if (entry.getKey().equals(activity) || entry.getValue().contains(activity) && entry.getValue().size() > 1) {
                    groupWithCurrentActivity = entry.getKey();
                    break;
                }
            }

            // If a group with the current 'activity' was found
            if (groupWithCurrentActivity != null) {
                // Check if the activityCount or activityTimestamp has changed for the representative of the group
                Integer currentCount = activityCount.get(activity);
                String currentTimestamp = activityTimestamp.get(activity);
                if (!currentCount.equals(lastActivityCount.get(activity)) || !currentTimestamp.equals(lastActivityTimestamp.get(activity))) {
                    // If the activityCount or activityTimestamp has changed, call reassessRepresentatives
                    clustering.reassessRepresentatives(activityCount, activityTimestamp);
                }
            }
        }

        previousMergeSet = mergeSet;
        mergeSet = clustering.getClusters();
        if (eachEventWriter != null) {
            try {
                Map<String, String> activityCluster = clustering.getActivityToCluster();
                String outputActivity = activityCluster.get(activity); // Get the output activity from the activityToCluster map
                String outputActivityValue = (outputActivity != null) ? outputActivity : activity;
                eachEventWriter.write((eventCounter-1) + ",");
                eachEventWriter.write(activity + ",");
                eachEventWriter.write(outputActivityValue + ",");
                eachEventWriter.write(activityCount.toString() + ",");
                eachEventWriter.write(mergeSet + "\n");
                eachEventWriter.flush();
            } catch (IOException e) {
                // System.out.println("Error occurred while writing to the file: " + e.getMessage());
            }
        }
        lastActivityCount = new HashMap<>(activityCount);
        lastActivityTimestamp = new HashMap<>(activityTimestamp);

        //System.out.println("Merge Set: " + mergeSet);
        // System.out.println();
        Instant end = Instant.now();

        // Calculate the processing time for this event
        Duration processingTime = Duration.between(start, end);

        // Update the total processing time and event count
        totalProcessingTime = totalProcessingTime.plus(processingTime);

        // Calculate and print the average processing time
        Duration averageProcessingTime = totalProcessingTime.dividedBy((long) eventCounter);
//        System.out.println("Average processing time per event: " + averageProcessingTime.toNanos() + " nanoseconds");



    }
    public void closeFile() {
        try {
            eachEventWriter.close();
            //forgetTriggeredWriter.close();
        } catch (IOException e) {
            // System.out.println("Error occurred while closing the file: " + e.getMessage());
        }
    }

    private void saveFootprintMatrixToCSV(String fileName) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName, true))) { // Set append to true
            writer.write("Event Counter: " + eventCounter);
            writer.newLine();
            for (int i = 0; i < footprintMatrix.length; i++) {
                String activity = getActivityFromIndex(i);
                writer.write("Activity " + activity + " (Index " + i + "): ");
                for (int j = 0; j < footprintMatrix[i].length; j++) {
                    writer.write(footprintMatrix[i][j] + ",");
                }
                writer.newLine();
            }
            writer.newLine(); // Add an extra newline to separate different matrices
            writer.flush();
        } catch (IOException e) {
            System.err.println("Error occurred while saving the footprint matrix to a CSV file: " + e.getMessage());
        }
    }

    // Forgetting Case if less than window size
    private Set<UniquePair> forgetCases() {
        Iterator<Map.Entry<String, int[]>> iterator = caseActivityIndices.entrySet().iterator();
        Set<UniquePair> pairs = new HashSet<>();
        while (iterator.hasNext()) {
            Map.Entry<String, int[]> entry = iterator.next();
            int caseIdCounter = entry.getValue()[2];
            if (caseIdCounter <= (cThreshold - delay)) {
                //print the caseId and activity to be removed
                // System.out.println("Case to be removed: " + entry.getKey() + " => Case details | Previous Activity: "+ entry.getValue()[0] + " | Current Activity: " + entry.getValue()[1]+ " | counter: "+ entry.getValue()[2]);
                // Remove from caseActivityIndices
                iterator.remove();

                // Remove from directlyFollows
                for (int i = 0; i < directlyFollows.length; i++) {
                    for (int j = 0; j < directlyFollows[i].length; j++) {
                        if (directlyFollows[i][j] != null && directlyFollows[i][j].containsKey(entry.getKey())) {
                            // save i, j int values as a pair
                            pairs.add(new UniquePair(i, j));
                            directlyFollows[i][j].remove(entry.getKey());
                        }
                    }
                }
                // Remove from activityIndices and decrement activityCount
                for (Map.Entry<String, HashMap<String, Integer>> activityEntry : activityIndices.entrySet()) {
                    Integer removedCount = activityEntry.getValue().remove(entry.getKey());
                    if (removedCount != null) {
                        activityCount.put(activityEntry.getKey(), activityCount.get(activityEntry.getKey()) - removedCount);
                    }
                }
            }
        }
        // System.out.println("Directly Follows Activity Index pairs affected by forgetting: " + pairs);
        return pairs;
    }
    private HashMap<String, Integer>[][] resizeMatrix(HashMap<String, Integer>[][] matrix, int newSize) {
        HashMap<String, Integer>[][] newMatrix = new HashMap[newSize][newSize];
        for (int i = 0; i < matrix.length; i++) {
            System.arraycopy(matrix[i], 0, newMatrix[i], 0, matrix[i].length);
        }
        return newMatrix;
    }
    private int[][] resizeFootprintMatrix(int[][] matrix, int newSize) {
        int[][] newMatrix = new int[newSize][newSize];
        for (int i = 0; i < matrix.length; i++) {
            System.arraycopy(matrix[i], 0, newMatrix[i], 0, matrix[i].length);
        }
        return newMatrix;
    }
    public int[][] getFootprintMatrix() {
        // Create a new matrix to hold the copy
        int[][] copy = new int[footprintMatrix.length][];
        for (int i = 0; i < footprintMatrix.length; i++) {
            // Copy each row into the new matrix
            copy[i] = footprintMatrix[i].clone();
        }
        return copy;
    }
    public HashMap<String, Integer> getActivityToIndex() {
        return new HashMap<>(this.activityToIndex);
    }
    public Map<String, List<String>> getMergeSet() {
        return mergeSet;
    }
    public List<Integer> findSimilarValuesInColumn(int columnIndex, int value, int skipIndex) {
        List<Integer> indices = new ArrayList<>();
        for (int i = 0; i < footprintMatrix.length; i++) {
            if (i == skipIndex) {
                continue;
            }
            if (footprintMatrix[i][columnIndex] == value) {
                indices.add(i);
            }
        }
        return indices;
    }
    private List<Integer> findAndAddSimilarValues(int prevIndex, int prevValue, int currentValue, int skipIndex) {
        List<Integer> xPrev = findSimilarValuesInColumn(prevIndex, prevValue, skipIndex);
        List<Integer> xCurrent = findSimilarValuesInColumn(prevIndex, currentValue, skipIndex);
        List<Integer> x = new ArrayList<>();
        x.addAll(xPrev);
        x.addAll(xCurrent);
        return x;
    }
    // similarity calculation method
    private Map.Entry<Integer, Float> calculateSimilarity(int i, int k) {
        int similarity = 0;
        int countI = 0;
        int countK = 0;
        for (int j = 0; j < footprintMatrix.length; j++) {
            if (footprintMatrix[i][j] != 0) {
                countI++;
            }
            if (footprintMatrix[k][j] != 0) {
                countK++;
            }
            if (footprintMatrix[i][j] != 0 && footprintMatrix[k][j] != 0 && footprintMatrix[i][j] == footprintMatrix[k][j]) {
                similarity++;
            }
        }
        float similarityValue = (float) similarity / Math.max(countI, countK) ;
        //if similarityValue is NaN
        if (Float.isNaN(similarityValue)) {
            similarityValue = 0;
        }

//        // System.out.println("Similar relations between "+i+" & "+k+": " + similarity + " -> Similarity:" + similarityValue + "| 1st activity relations " + countI + ": 2nd activity relations: " + countK);


        return new AbstractMap.SimpleEntry<>(k, similarityValue);
    }
    private void checkForMergeUnmerge(List<Integer> indices, int i) {
        List<SimilarityResult> simIndex = new ArrayList<>();
        for (int k : indices) {
            if (i != k) {
                Map.Entry<Integer, Float> similarity = calculateSimilarity(i, k);
                ActivityPair pair = new ActivityPair(i, k);
                Float existingSimilarity = similarityMap.get(pair);
                if (existingSimilarity == null || !existingSimilarity.equals(similarity.getValue())) {
                    // System.out.println("Similarity value: " + similarity.getValue() + " for " + getActivityFromIndex(i) + " with " + getActivityFromIndex(k));
                    similarityMap.put(pair, similarity.getValue());
                    clustering.addSimilarity(getActivityFromIndex(i), getActivityFromIndex(k), similarity.getValue(), activityCount, activityTimestamp);
                    // Re-cluster with the updated data
                    clustering.clusterActivities();
                    clustering.reassessRepresentatives(activityCount, activityTimestamp);
                    clusteringHappen = true;
                }


//                if ((similarity.getValue() >= controlFlowSimThreshold && existingSimilarity < controlFlowSimThreshold) || (similarity.getValue() < controlFlowSimThreshold && existingSimilarity >= controlFlowSimThreshold)){
//                    // System.out.println("Error Occuring Place");
////                   simIndex.add(new SimilarityResult(i, k, similarity.getValue()));
////                   similarityMap.put(pair, similarity.getValue());
//
//                    //Incremental Hierarchical Clustering for Merge and Unmerge
//                    clustering.addSimilarity(getActivityFromIndex(i), getActivityFromIndex(k), similarity.getValue());
//                    // Re-cluster with the updated data
//                    clustering.clusterActivities();
//                    clustering.reassessRepresentatives();
//                    clustering.printClusters();
//                    // System.out.println(clustering.getAdjacencyList());
//                }
            }
        }
//        return simIndex;
    }


//    private HashMap<ActivityPair, Float> overThresholdControlSimilarityMap() {
//        HashMap<ActivityPair, Float> overThresholdSimilarityMap = new HashMap<>();
//        for (Map.Entry<ActivityPair, Float> entry : similarityMap.entrySet()) {
//            if (entry.getValue() >= controlFlowSimThreshold) {
//                overThresholdSimilarityMap.put(entry.getKey(), entry.getValue());
//            }
//        }
//        return overThresholdSimilarityMap;
//    }
//    private void clusterMergeUnmerge(float eps, int minPts) {
//        HashMap<ActivityPair,Float> overThresholdSimilarityMap = overThresholdControlSimilarityMap();
//        // Create a new DBSCAN object with the similarityMap, eps = 0.5, and minPts = 2
//        DBSCAN dbscan = new DBSCAN(overThresholdSimilarityMap, eps, minPts);
//        // Run DBSCAN and get the clusters
//        Set<Set<Integer>> clusters = dbscan.apply();
//        // System.out.println(clusters);
//        // Print the centroids and their elements
//        dbscan.printCentroidsAndElements();
//        mergeSet = dbscan.getCentroidsAndElements();
//        // System.out.println("Updating the merge list: " + mergeSet);
//
//    }



    private void printAndCalculateSimilarities(int prevActivityIndex, int currentActivityIndex, List<Integer> xA, List<Integer> xB) {
        // System.out.println("Activity indexes to check the changed similarity with (X_b) " + getActivityFromIndex(currentActivityIndex) + " is: " + xA);
        checkForMergeUnmerge(xA, currentActivityIndex);
        // System.out.println("Activity indexes to check the changed similarity with (X_a) " + getActivityFromIndex(prevActivityIndex) + " is: " +  xB);
        checkForMergeUnmerge(xB, prevActivityIndex);
//        // System.out.println("xASimilarity: " + xAChangedSimilarity);
//        // System.out.println("xBSimilarity: " + xBChangedSimilarity);
//        List<SimilarityResult> combinedChangedSimilarity = new ArrayList<>();
//        combinedChangedSimilarity.addAll(xAChangedSimilarity);
//        combinedChangedSimilarity.addAll(xBChangedSimilarity);
//        // System.out.println("Combined similarity: " + combinedChangedSimilarity);
//          clusterMergeUnmerge(0.2F, 1);

    }

    private void footprintUpdate(int prevActivityIndex, int currentActivityIndex) {
        prevFootprint = footprintMatrix;
        if (prevActivityIndex != -1) {
            int countXY = directlyFollows[prevActivityIndex][currentActivityIndex] != null ? directlyFollows[prevActivityIndex][currentActivityIndex].values().stream().mapToInt(Integer::intValue).sum() : 0;
            int countYX = directlyFollows[currentActivityIndex][prevActivityIndex] != null ? directlyFollows[currentActivityIndex][prevActivityIndex].values().stream().mapToInt(Integer::intValue).sum() : 0;
            // System.out.println(getActivityFromIndex(prevActivityIndex)+" directly follows " + getActivityFromIndex(currentActivityIndex) + ": Count of '" + getActivityFromIndex(prevActivityIndex) + "' followed by '" +  getActivityFromIndex(currentActivityIndex) + "': " + countXY + " Count of '" + getActivityFromIndex(currentActivityIndex) + "' followed by '" + getActivityFromIndex(prevActivityIndex) + "': " +countYX);
            float causalityValue = (float) (countXY - countYX) / (countXY + countYX + 1);
            // System.out.println("Causality value: " + causalityValue);
            // Calculate parallelismValue
            float parallelismValue = (float) Math.max(countXY, countYX) / Math.min(countXY, countYX);
            //// System.out.println("Activity count: " + activityCount.get(getActivityFromIndex(prevActivityIndex)) + ", " + activityCount.get(getActivityFromIndex(currentActivityIndex)));
            //float parallelismValue = (float) (2 * (countXY + countYX)) / (activityCount.get(getActivityFromIndex(prevActivityIndex)) + activityCount.get(getActivityFromIndex(currentActivityIndex)));
            // System.out.println("Parallelism value: " + parallelismValue);

            //get the value of the footprint matrix before updating it, if it's not available its 0
            int prevValueA = footprintMatrix[currentActivityIndex][prevActivityIndex];
            int prevValueB = footprintMatrix[prevActivityIndex][currentActivityIndex];

            // !important
            //xA - current index similar values (remove current index from the list of similar values)
            //xB - previous index similar values (remove previous index from the list of similar values)

            // Check if value is larger than 0.8 or smaller than -0.8
            if (Math.abs(causalityValue) >= upperCausalityThreshold) {
                // Determine if the value is positive or negative

                float sign = Math.signum(causalityValue);
                if (sign > 0) {
                    if (prevValueB != 1) {
                        footprintMatrix[prevActivityIndex][currentActivityIndex] = 1;
                        footprintMatrix[currentActivityIndex][prevActivityIndex] = 2;
                        // System.out.println("Value is positive and larger than 0.8");
                        List<Integer> xA = findAndAddSimilarValues(prevActivityIndex, prevValueA, 2,currentActivityIndex);
                        List<Integer> xB = findAndAddSimilarValues(currentActivityIndex, prevValueB, 1,prevActivityIndex);
                        printAndCalculateSimilarities(prevActivityIndex, currentActivityIndex, xA, xB);
                    }
                } else if (sign < 0) {
                    if (prevValueB != 2) {
                        footprintMatrix[prevActivityIndex][currentActivityIndex] = 2;
                        footprintMatrix[currentActivityIndex][prevActivityIndex] = 1;
                        // System.out.println("Value is negative and smaller than -0.8");
                        List<Integer> xA = findAndAddSimilarValues(prevActivityIndex, prevValueA, 1,currentActivityIndex);
                        List<Integer> xB = findAndAddSimilarValues(currentActivityIndex, prevValueB, 2,prevActivityIndex);
                        printAndCalculateSimilarities(prevActivityIndex, currentActivityIndex, xA, xB);
                    }
                }
            } else if (parallelismValue <= upperParallelismThreshold) {
                if (prevValueB != 3) {
                    footprintMatrix[prevActivityIndex][currentActivityIndex] = 3;
                    footprintMatrix[currentActivityIndex][prevActivityIndex] = 3;
                    // System.out.println("Value is greater or equal than 0.8");
                    List<Integer> xA = findAndAddSimilarValues(prevActivityIndex, prevValueA, 3, currentActivityIndex);
                    List<Integer> xB = findAndAddSimilarValues(currentActivityIndex, prevValueB, 3, prevActivityIndex);
                    printAndCalculateSimilarities(prevActivityIndex, currentActivityIndex, xA, xB);
                }
            } else if (Math.abs(causalityValue) < lowerCausalityThreshold || parallelismValue >= lowerParallelismThreshold) {
                if (prevValueB != 0) {
                    footprintMatrix[prevActivityIndex][currentActivityIndex] = 0;
                    footprintMatrix[currentActivityIndex][prevActivityIndex] = 0;
                    // System.out.println("Absolute value is smaller than 0.7 for causality or parallelism");
                    List<Integer> xA = findAndAddSimilarValues(prevActivityIndex, prevValueA, 0, currentActivityIndex);
                    List<Integer> xB = findAndAddSimilarValues(currentActivityIndex, prevValueB, 0, prevActivityIndex);
                    printAndCalculateSimilarities(prevActivityIndex, currentActivityIndex, xA, xB);
                }
            }
            // print the count
            //print footprint matrix
            //// System.out.println("Footprint matrix: " + Arrays.deepToString(footprintMatrix));
        }
    }

    public String getActivityFromIndex(int index) {
        for (Map.Entry<String, Integer> entry : activityToIndex.entrySet()) {
            if (entry.getValue().equals(index)) {
//                // System.out.println("## Activity from index: ##"+entry.getKey());
                return entry.getKey();
            }
        }
        return null;
    }
    String convertDirectlyFollowsToJson() {
        Gson gson = new Gson();
        int[][] directlyFollowsSum = new int[directlyFollows.length][directlyFollows[0].length];
        for (int i = 0; i < directlyFollows.length; i++) {
            for (int j = 0; j < directlyFollows[i].length; j++) {
                if (directlyFollows[i][j] != null) {
                    directlyFollowsSum[i][j] = directlyFollows[i][j].values().stream().mapToInt(Integer::intValue).sum();
                }
            }
        }
        return gson.toJson(directlyFollowsSum);
    }

    private void printFootprintMatrix(int[][] matrix) {
        System.out.print("    "); // Space for row indices
        for (int i = 0; i < matrix[0].length; i++) {
            String activity = getActivityFromIndex(i);
            System.out.print(activity + " ");
        }
        System.out.println();

        for (int i = 0; i < matrix.length; i++) {
            String activity = getActivityFromIndex(i);
            System.out.print(activity + " : "); // Row index
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println(); // Move to the next line after printing each row
        }
        System.out.println("Event Counter: " + eventCounter);
    }


}
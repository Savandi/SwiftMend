package com.tievs.swiftmend.utils;

import java.util.*;

public class DBSCAN {
    private HashMap<Integer, List<Float>> distanceMap = new HashMap<>();
    private double eps;
    private int minPts;
    private HashMap<Set<Integer>, Integer> centroids = new HashMap<>();
    private HashMap<ActivityPair, Float> similarityMap;

    public DBSCAN(HashMap<ActivityPair, Float> similarityMap, double eps, int minPts) {
        this.eps = eps;
        this.minPts = minPts;
        this.similarityMap = similarityMap;

        for (Map.Entry<ActivityPair, Float> entry : similarityMap.entrySet()) {
            ActivityPair pair = entry.getKey();
            float distance = 1 - entry.getValue();

            distanceMap.computeIfAbsent(pair.getActivityIndex1(), k -> new ArrayList<>()).add(distance);
            distanceMap.computeIfAbsent(pair.getActivityIndex2(), k -> new ArrayList<>()).add(distance);
        }
    }

    public Set<Set<Integer>> apply() {
        Set<Set<Integer>> clusters = new HashSet<>();
        Set<Integer> visited = new HashSet<>();

        for (Integer index : distanceMap.keySet()) {
            if (!visited.contains(index)) {
                visited.add(index);
                List<Integer> neighbors = getNeighbors(index);
                if (neighbors.size() >= minPts) {
                    Set<Integer> cluster = new HashSet<>();
                    expandCluster(index, neighbors, cluster, visited);
                    // Only add clusters with more than one element to the result
                    if (cluster.size() > 1) {
                        clusters.add(cluster);
                    }
                }
            }
        }

        for (Set<Integer> cluster : clusters) {
            int centroid = getCentroid(cluster);
            centroids.put(cluster, centroid);
        }

        return clusters;
    }

    private void expandCluster(Integer index, List<Integer> neighbors, Set<Integer> cluster, Set<Integer> visited) {
        cluster.add(index);

        for (int i = 0; i < neighbors.size(); i++) {
            Integer neighbor = neighbors.get(i);
            if (!visited.contains(neighbor)) {
                visited.add(neighbor);
                List<Integer> neighborNeighbors = getNeighbors(neighbor);
                if (neighborNeighbors.size() >= minPts) {
                    neighbors.addAll(neighborNeighbors);
                }
            }
            // Only add the neighbor to the cluster if the distance is less than or equal to eps
            if (!cluster.contains(neighbor) && getDistance(index, neighbor) <= eps) {
                cluster.add(neighbor);
            }
        }
    }

    private List<Integer> getNeighbors(Integer index) {
        List<Integer> neighbors = new ArrayList<>();
        for (ActivityPair pair : similarityMap.keySet()) {
            if (pair.getActivityIndex1() == index && getDistance(index, pair.getActivityIndex2()) <= eps) {
                neighbors.add(pair.getActivityIndex2());
            } else if (pair.getActivityIndex2() == index && getDistance(index, pair.getActivityIndex1()) <= eps) {
                neighbors.add(pair.getActivityIndex1());
            }
        }
        return neighbors;
    }

    private float getDistance(Integer index1, Integer index2) {
        List<Float> distances1 = distanceMap.get(index1);
        List<Float> distances2 = distanceMap.get(index2);

        if (distances1 == null || distances2 == null) {
            return Float.MAX_VALUE;
        }

        float minDistance = Float.MAX_VALUE;
        for (Float distance1 : distances1) {
            for (Float distance2 : distances2) {
                float distance = Math.abs(distance1 - distance2);
                if (distance < minDistance) {
                    minDistance = distance;
                }
            }
        }

        return minDistance;
    }

    public void printCentroidsAndElements() {
        for (Map.Entry<Set<Integer>, Integer> entry : centroids.entrySet()) {
            Set<Integer> cluster = entry.getKey();
            Integer centroid = entry.getValue();

            System.out.println("Centroid: " + centroid);

            Set<Integer> elements = new HashSet<>(cluster);
            elements.remove(centroid);

            System.out.println("Elements: " + elements);
        }
    }
    public HashMap<Integer, int[]> getCentroidsAndElements() {
        HashMap<Integer, int[]> result = new HashMap<>();

        for (Map.Entry<Set<Integer>, Integer> entry : centroids.entrySet()) {
            Set<Integer> cluster = entry.getKey();
            Integer centroid = entry.getValue();

            Set<Integer> elements = new HashSet<>(cluster);
            elements.remove(centroid);

            int[] elementsArray = elements.stream().mapToInt(i->i).toArray();

            result.put(centroid, elementsArray);
        }

        return result;
    }
    private int getCentroid(Set<Integer> cluster) {
        int centroid = -1;
        int maxRelations = -1;

        for (Integer index : cluster) {
            int relations = 0;
            for (ActivityPair pair : similarityMap.keySet()) {
                if ((pair.getActivityIndex1() == index && cluster.contains(pair.getActivityIndex2())) ||
                        (pair.getActivityIndex2() == index && cluster.contains(pair.getActivityIndex1()))) {
                    relations++;
                }
            }
            if (relations > maxRelations) {
                maxRelations = relations;
                centroid = index;
            }
//            else if (relations == maxRelations && 2 > 1) {
//                centroid = index;
//            }
        }

        return centroid;
    }
}
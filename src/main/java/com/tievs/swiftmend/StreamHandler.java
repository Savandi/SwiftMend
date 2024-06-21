package com.tievs.swiftmend;

import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.concurrent.CopyOnWriteArrayList;

import org.json.JSONObject;

public class StreamHandler extends Thread {
    private CopyOnWriteArrayList<String> caseIDs = new CopyOnWriteArrayList<>();
    private ControlFlowStreamSimilarityCalculation processMiningHandler = new ControlFlowStreamSimilarityCalculation();
    private final String port = System.getProperty("port");
    public void run() {
        while (true) {
            try {
                URL url = new URL("http://localhost:"+port+"/stream"); // Flask app URL
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                con.setRequestMethod("GET");

                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                while ((inputLine = in.readLine()) != null) {
                    JSONObject obj = new JSONObject(inputLine);
                    String caseID = obj.getString("case");
                    String activity = obj.getString("event");
                    String timestamp = obj.getString("completeTime");
                    if (caseIDs.addIfAbsent(caseID)) {
//                        System.out.println("New caseID added: " + caseID);
//                        System.out.println("Current caseIDs: " + caseIDs);
//                        System.out.println();
                    }
                    processMiningHandler.processActivity(caseID, activity, timestamp);
                }
                in.close();
                processMiningHandler.closeFile();
            } catch (Exception e) {
                System.out.println("Error occurred: " + e.getMessage());
            }

            try {
                Thread.sleep(1000); // Wait for 1 seconds before retrying
            } catch (InterruptedException ie) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public CopyOnWriteArrayList<String> getCaseIDs() {
        return caseIDs;
    }

    public ControlFlowStreamSimilarityCalculation getProcessMiningHandler() {
        return processMiningHandler;
    }
}
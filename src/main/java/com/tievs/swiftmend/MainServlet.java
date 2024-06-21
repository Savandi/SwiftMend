package com.tievs.swiftmend;

import com.google.gson.Gson;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@WebServlet(name = "MainServlet", value = "/")
public class MainServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        StreamHandler streamHandler = (StreamHandler) getServletContext().getAttribute("streamHandler");
        List<String> caseIDs = streamHandler.getCaseIDs();

        String path = request.getRequestURI();

        switch (path) {
            case "/cases":
                response.setContentType("application/json");
                response.setCharacterEncoding("UTF-8");
                response.setHeader("Access-Control-Allow-Origin", "*"); // Allow AJAX requests from any origin
                PrintWriter out = response.getWriter();
                out.print(caseIDs.toString());
                out.flush();
                break;
            case "/footprint":
                response.setContentType("application/json");
                response.setCharacterEncoding("UTF-8");
                response.setHeader("Access-Control-Allow-Origin", "*"); // Allow AJAX requests from any origin
                out = response.getWriter();
                int[][] footprintMatrix = streamHandler.getProcessMiningHandler().getFootprintMatrix();
                out.print(Arrays.deepToString(footprintMatrix));
                out.flush();
                break;
            case "/distinctActivities":
                response.setContentType("application/json");
                response.setCharacterEncoding("UTF-8");
                response.setHeader("Access-Control-Allow-Origin", "*"); // Allow AJAX requests from any origin
                out = response.getWriter();
                HashMap<String, Integer> activityToIndex = streamHandler.getProcessMiningHandler().getActivityToIndex();
                Gson gson = new Gson();
                String json = gson.toJson(activityToIndex);
                out.print(json);
                out.flush();
                break;
            case "/clusters":
                response.setContentType("application/json");
                response.setCharacterEncoding("UTF-8");
                response.setHeader("Access-Control-Allow-Origin", "*"); // Allow AJAX requests from any origin
                out = response.getWriter();
                Map<String, List<String>> centroidsAndElements = streamHandler.getProcessMiningHandler().getMergeSet();
                gson = new Gson();
                json = gson.toJson(centroidsAndElements);
                out.print(json);
                out.flush();
                break;
            case "/directlyFollows":
                response.setContentType("application/json");
                response.setCharacterEncoding("UTF-8");
                response.setHeader("Access-Control-Allow-Origin", "*"); // Allow AJAX requests from any origin
                out = response.getWriter();
                String directlyFollowsJson = streamHandler.getProcessMiningHandler().convertDirectlyFollowsToJson();
                out.print(directlyFollowsJson);
                out.flush();
                break;
//            default:
//                // Handle unknown paths
//                break;
        }
    }
}
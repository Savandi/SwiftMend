//package com.tievs.swiftmend.utils;
//import moa.src.main.java.moa.clusterers.denstream.*;
//import com.yahoo.labs.samoa.instances.DenseInstance;
//import com.yahoo.labs.samoa.instances.Instance;
//import com.yahoo.labs.samoa.instances.Instances;
//import com.yahoo.labs.samoa.instances.InstancesHeader;
//import com.yahoo.labs.samoa.instances.Attribute;
//import moa.core.FastVector;
//
//public class DenStream {
//    public static void main(String[] args) {
//        // Initialize DenStream
//        DBSCAN denStream = new moa.clusterers.macro.dbscan.DBScan();
//
//        // Define the data stream structure
//        FastVector<Attribute> attributes = new FastVector<>();
//        attributes.addElement(new Attribute("feature1"));
//        attributes.addElement(new Attribute("feature2"));
//        attributes.addElement(new Attribute("feature3"));
//
//        InstancesHeader streamHeader = new InstancesHeader(new Instances("Stream", attributes, 0));
//        streamHeader.setClassIndex(streamHeader.numAttributes() - 1);
//
//        denStream.setModelContext(streamHeader);
//        denStream.prepareForUse();
//
//        // Creating example data points
//        double[][] points = new double[][]{
//                {1.0, 0.8, 0.5}, // Activity 0
//                {0.8, 1.0, 0.6}, // Activity 1
//                {0.5, 0.6, 1.0}  // Activity 2
//        };
//
//        // Process each data point
//        for (double[] point : points) {
//            Instance inst = new DenseInstance(1.0, point);
//            inst.setDataset(streamHeader);
//            denStream.trainOnInstanceImpl(inst);
//        }
//
//        // Output the clustering result
//        System.out.println(denStream.getMicroClusteringResult());
//    }
//}
//

package com.tievs.swiftmend.utils;

import org.python.core.PyDictionary;
import org.python.core.PyList;
import org.python.core.PyTuple;
import org.python.util.PythonInterpreter;

import java.util.List;
import java.util.ArrayList;

public class JythonIntegration {
    public static void performDENSTREAMClustering(List<SimilarityResult> similarities) {
        // Convert Java list to Python list of tuples or dictionaries
        PythonInterpreter interpreter = new PythonInterpreter();
        PyList pyList = new PyList();

        for (SimilarityResult result : similarities) {
            // Convert each SimilarityResult object to a Python dictionary
            PyDictionary pyDict = new PyDictionary();
            pyDict.put("i", result.getI());
            pyDict.put("k", result.getK());
            pyDict.put("similarityValue", result.getSimilarityValue());
            pyList.add(pyDict);
        }

        // Pass the Python list to your Python script
        interpreter.set("similarities", pyList);
        interpreter.execfile("python/your_python_script.py");
    }
}

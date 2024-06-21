package com.tievs.swiftmend;

import jakarta.servlet.ServletContextEvent;
import jakarta.servlet.ServletContextListener;
import jakarta.servlet.annotation.WebListener;

@WebListener
public class ContextListener implements ServletContextListener {

    private StreamHandler streamHandler;

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        streamHandler = new StreamHandler();
        sce.getServletContext().setAttribute("streamHandler", streamHandler);
        streamHandler.start();
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        if (streamHandler != null) {
            streamHandler.interrupt();
        }
    }
}
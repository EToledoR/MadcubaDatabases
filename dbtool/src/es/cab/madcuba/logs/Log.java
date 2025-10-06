package es.cab.madcuba.log;

import org.apache.log4j.Logger;

/**
 * Shim simple de Log (singleton) para aprovechar log4j-1.2.x.
 */
public final class Log {
    private static final Log INSTANCE = new Log();
    public final Logger logger;

    private Log() {
        this.logger = Logger.getLogger("MADCUBA");
    }

    public static Log getInstance() {
        return INSTANCE;
    }
}


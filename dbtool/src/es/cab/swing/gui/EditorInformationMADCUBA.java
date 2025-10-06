package es.cab.swing.gui;

/**
 * Shim no-UI: redirige mensajes a consola para el CLI.
 */
public final class EditorInformationMADCUBA {
    private EditorInformationMADCUBA() {}

    public static void appendLineError(String msg) {
        System.err.println(msg);
    }

    public static void append(String msg) {
        System.out.print(msg);
    }
}


package es.cab.madcuba.utils;

/**
 * Shim mínimo para compilar el dbtool fuera de MADCUBA.
 * Ponemos valores neutros/legibles. Si necesitas etiquetas exactas
 * de UI más adelante, se pueden ajustar aquí sin tocar el resto.
 */
public final class MyConstants {
    private MyConstants() {}

    public static final String LABEL_DELTA_NO_MAC = "Δ";
    public static final String LABEL_DELTA_MAC    = "Δ*";

    public static final String LABEL_TAU_NO_MAC_OLD = "tau";
    public static final String LABEL_TAU_MAC_OLD    = "tau*";

    // Usado en SlimConstants como cabecera
    public static final String HEADER_SLIM_SLIM = "SLIM";
}


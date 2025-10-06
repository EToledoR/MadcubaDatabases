package es.smr.slim;

import java.nio.file.*;
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;

public class DbHSQLDBCreateCLI {

  private static void usage() {
    System.out.println(
      "Uso:\n" +
      "  java -jar madcuba-dbtool-standalone.jar --db <DB_PATH> [--standalone] [--userdb <PATH>] [--clean]\n\n" +
      "Ejemplos:\n" +
      "  java -jar madcuba-dbtool-standalone.jar --db ./lines --clean\n" +
      "  java -jar madcuba-dbtool-standalone.jar --db /data/lines --userdb /data/extradb --standalone\n"
    );
  }

  public static void main(String[] args) {
    try {
      // Log básico
      BasicConfigurator.configure();
      Logger.getRootLogger().setLevel(Level.INFO);
      System.setProperty("java.awt.headless", "true");

      String dbPath = null;          // equivalente a tu 'dbPath' (p.ej. "./lines")
      boolean standalone = false;    // tu segundo parámetro del constructor
      boolean clean = false;         // borrar/comenzar de cero (opcional)
      String userDbRoot = null;      // ruta para CreateUSERdatabase (opcional)

      for (int i = 0; i < args.length; i++) {
        switch (args[i]) {
          case "--db": dbPath = args[++i]; break;
          case "--standalone": standalone = true; break;
          case "--clean": clean = true; break;
          case "--userdb": userDbRoot = args[++i]; break;
          case "-h": case "--help": usage(); return;
          default:
            System.err.println("Argumento no reconocido: " + args[i]);
            usage(); return;
        }
      }
      if (dbPath == null) { System.err.println("Falta --db <DB_PATH>"); usage(); return; }

      Path p = Paths.get(dbPath);
      if (!Files.exists(p)) {
        // Si quieres replicar el comportamiento original (crear ./lines si no existe),
        // puedes crear la carpeta:
        Files.createDirectories(p);
      }

      System.out.println("[DBTOOL] dbPath=" + p.toAbsolutePath()
          + " standalone=" + standalone + " clean=" + clean
          + (userDbRoot != null ? " userdb=" + userDbRoot : ""));

      // Construye como en tu main: new DbHSQLDBCreate(dbPath, true);
      DbHSQLDBCreate tool = new DbHSQLDBCreate(p.toString(), standalone);

      // Llama a la nueva orquestación (equivalente a tu main)
      tool.createAllCatalogs(clean, /*isUserDB=*/false, userDbRoot);

      System.out.println("[DBTOOL] Hecho.");
    } catch (Exception ex) {
      ex.printStackTrace();
      System.exit(1);
    }
  }
}


class Geogebra():
    def ausgabeJavascript(self, window_height, window_width, befehle, size_coord = [-6,6,-4,4], draw_grid=True):
        try:
            size_coord_string = "ggbApplet.setCoordSystem(%f,%f,%f,%f);" % ([a for a in size_coord])
        except:
            size_coord_string = "ggbApplet.setCoordSystem(-6,6,-4,4);"

        if draw_grid:
            draw_grid_string = "ggbApplet.setGridVisible(true);"
        else:
            draw_grid_string = "ggbApplet.setGridVisible(false);"
        ausgabe = """
        <meta name=viewport content="width=device-width,initial-scale=1">  
        <meta charset="utf-8"/>
        <script src="https://www.geogebra.org/apps/deployggb.js"></script>
        <script>  
            var params = {"appName": "classic", "material_id": "pb85ndew", "width": %d, "height": %d, "showToolBar": false, "showAlgebraInput": true, "showMenuBar": false, "useBrowserForJS": true};
            var applet = new GGBApplet(params, true); 

            window.addEventListener("load", function() { 
                applet.inject('ggb-element');
            });

            function ggbOnInit() {
                %s
                %s
                %s
            }
        </script>    
        <div id="ggb-element"></div> 
        """ % (window_width, window_height, draw_grid_string, size_coord_string, self.geogebraBefehl(befehle))
        return ausgabe
    
    def ausgabeJavascript3d(self, window_height, window_width, befehle):
        ausgabe = """
        <meta name=viewport content="width=device-width,initial-scale=1">  
        <meta charset="utf-8"/>
        <script src="https://www.geogebra.org/apps/deployggb.js"></script>
        <script>  
            var params = {"appName": "3d", "material_id": "kb9nnzsh", "width": %d, "height": %d, "showToolBar": false, "showAlgebraInput": false, "showMenuBar": false, "useBrowserForJS": true};
            var applet = new GGBApplet(params, true); 

            window.addEventListener("load", function() { 
                applet.inject('ggb-element');
            });

            function ggbOnInit() {
                %s
            }
        </script>    
        <div id="ggb-element"></div> 
        """ % (window_width, window_height, self.geogebraBefehl(befehle))
        return ausgabe

    def geogebraBefehl(self, eingabe):
        ausgabe  = ""
        for befehl in eingabe:
            ausgabe += "ggbApplet.evalCommand('%s');\n" % (befehl)
        return ausgabe[:-1]
    
    def ebene3d(self, name, normalenvektor, parameterd):
        return "%s = Plane(%f*x+%f*y+%f*z=%f)" % (name, normalenvektor[0], normalenvektor[1], normalenvektor[2], parameterd)
    
    def punkt3d(self, name, koordinaten):
        return "%s = (%f,%f,%f)" % (name, koordinaten[0], koordinaten[1], koordinaten[2])
    
    def punkt3dsp(self, name, koordinaten):
        return "%s = (%f,%f,%f)" % (name, koordinaten.x, koordinaten.y, koordinaten.z)
    
    def gerade3d(self, name, punkt1, punkt2):
        return "%s = Line((%f,%f,%f),(%f,%f,%f))" % (name, punkt1[0], punkt1[1], punkt1[2], punkt2[0], punkt2[1], punkt2[2])

    def gerade3dsp(self, name, gerade):
        return "%s = Line((%f,%f,%f),(%f,%f,%f))" % (name, gerade.points[0][0], gerade.points[0][1], gerade.points[0][2], gerade.points[1][0], gerade.points[1][1], gerade.points[1][2])
    
    def farbe(self, name, farbe):
        return "SetColor(%s, %s)" % (name, farbe);
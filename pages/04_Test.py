import streamlit as st


def geogebraBefehl(eingabe):
    ausgabe  = ""
    for befehl in eingabe:
        ausgabe += "ggbApplet.evalCommand('%s');\n" % (befehl)
    return ausgabe

a = st.slider("amp", 0.1, 5.0, 0.1)

#befehle = geogebraBefehl(["a = Slider(1,5,0.1)","f(x)=a*sqrt(x)", '"f(x)=" + FormulaText(f)+""'])
befehle = geogebraBefehl(['a = Slider(0,5,0.1)', 'f(x) = a*x^2', 'FormulaText(f, true, true)', r'c=Checkbox({f,Text1})', r'd=Checkbox({a})', 'SetBackgroundColor(Text1, "#FFFFFFFF")', 'BinomialDist(5,0.2)', 'Normal(1,0.3,x,false)'])

window_width = 800
window_height = 600

js_text ="""
<meta name=viewport content="width=device-width,initial-scale=1">  
<meta charset="utf-8"/>
<script src="https://www.geogebra.org/apps/deployggb.js"></script>
<script>  
    var params = {"appName": "classic", "material_id": "pb85ndew", "width": %d, "height": %d, "showToolBar": false, "showAlgebraInput": false, "showMenuBar": false, "useBrowserForJS": true};
    var applet = new GGBApplet(params, true); 

    window.addEventListener("load", function() { 
        applet.inject('ggb-element');
    });

    function ggbOnInit() {
        ggbApplet.setGridVisible(true);
        ggbApplet.setCoordSystem(-6,6,-4,4);
        %s
        ggbApplet.setCoords("Text1", -5, 3);
        ggbApplet.setCoords("a", 500, 50);
        ggbApplet.registerAddListener("myAddListenerFunction"); 
        gbbApplet.setLabelStyle('f', 2)
        gbbApplet.setLabelVisible('f', true);
    }

    function myAddListenerFunction(name) {
        ggbApplet.evalCommand('C=(2,3)');
    }

</script>    
<div id="ggb-element"></div> 
""" % (window_width, window_height, befehle)

st.header("Geogebra in Streamlit")

st.components.v1.html(
js_text, height=window_height, width=window_width
)
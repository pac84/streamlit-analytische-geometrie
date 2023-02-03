import streamlit as st
#import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app

punktA = "f(x) = x^2"
test = "Derivative(f)"
window_width = 800
window_height = 600

js_text ="""
<meta name=viewport content="width=device-width,initial-scale=1">  
<meta charset="utf-8"/>
<script src="https://www.geogebra.org/apps/deployggb.js"></script>
<script>  
    var params = {"appName": "classic", "width": %d, "height": %d, "showToolBar": true, "showAlgebraInput": true, "showMenuBar": true, "useBrowserForJS": true};
    var applet = new GGBApplet(params, true); 

    window.addEventListener("load", function() { 
        applet.inject('ggb-element');
    });

    function ggbOnInit() {
        ggbApplet.evalCommand('%s');
        ggbApplet.evalCommand('%s');
    }

</script>    
<div id="ggb-element"></div> 
""" % (window_width, window_height, punktA, test)

st.header("Geogebra in Streamlit")

st.components.v1.html(
js_text, height=window_height, width=window_width
)
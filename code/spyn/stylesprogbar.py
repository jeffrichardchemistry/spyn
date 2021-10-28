class layoutsProgbar():
        def stylesProgbar(self):
            style1 = """
            QProgressBar{
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center
            }

            QProgressBar::chunk {
                background-color: lightblue;
                width: 10px;
                margin: 1px;
            }
            """

            style2 = """
            QProgressBar{
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            color: rgb(0, 0, 0);
            font: 75 italic 12pt "Roboto Condensed";
            }

            QProgressBar::chunk {
                background-color: green;
                width: 10px;
                margin: 1px;
            }
            """

            template_css = """QProgressBar::chunk { background: %s; }"""
            style3 = template_css % 'yelow' #trocar aqui a cor

            style4 = """QProgressBar:horizontal {
            border: 1px solid gray;
            border-radius: 3px;
            background: white;
            padding: 1px;
            }
            QProgressBar::chunk:horizontal {
            background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 green, stop: 1 white);       
            }"""

            style5 = """QProgressBar:horizontal {         
            border: 1px solid gray;
            border-radius: 3px;
            background: white;
            padding: 1px;
            text-align: center;
            margin-right: 4ex;            
            }
            
            QProgressBar::chunk:horizontal {               
            background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 green, stop: 1 white);
            margin-right: 2px; /* space */
            width: 10px;
            }"""

            style6 = """QProgressBar {
            border: 1.5px solid black;
            color: rgb(0, 0, 0);
            font: 75 italic 12pt "Roboto Condensed";
            text-align: top;
            padding: 1px;
            border-radius: 5px;
            background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #FFFF00,
            stop: 0.4999 #eee,
            stop: 0.5 #ddd,
            stop: 1 #eee );
            width: 15px;
            
             
            }

            QProgressBar::chunk {
            background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #FFFF00,
            stop: 0.4999 #FFFF00,
            stop: 0.5 #0084FE,
            stop: 1 #0084FE );                      
            }
            
            """            
            #border: 1px solid black;
            #border-bottom-right-radius: 7px;
            #border-bottom-left-radius: 7px;
            
            style7 = """QProgressBar::chunk {background: hsva(%1, 255, 255, 70%);}

            """
            
            return style1, style2, style3, style4, style5, style6, style7
            
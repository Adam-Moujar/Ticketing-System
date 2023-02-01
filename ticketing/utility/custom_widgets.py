from django import forms

import AdvancedHTMLParser
from AdvancedHTMLParser import AdvancedTag



class ClearableRadioSelect(forms.RadioSelect):

    def render(self, name, value, attrs = None, renderer = None):
        htmlResult = super(forms.RadioSelect, self).render(name, value, attrs, renderer)

        parser = AdvancedHTMLParser.AdvancedHTMLParser()

        parser.parseStr(htmlResult)

        labels = parser.getElementsByTagName("label")
        inputs = parser.getElementsByTagName("input")
        divs = parser.getElementsByTagName("div")

        #divs[0].addClass("btn-group")
        #divs[0].setStyle("display", "inline-block")


        parent = divs[0]

        for i in range(1, len(divs)):

            children = divs[i].getAllChildNodes()

            divs[i].remove()


        for i in range(0, len(labels)):
           #labels[i].addClass("btn btn-outline-primary")
           #inputs[i].addClass("btn-check")

           parent.appendChild(inputs[i])

           labels[i].removeChild(labels[i].firstChild)

           parent.appendChild(labels[i])


        parent.setStyle("padding-top", "0px;")
        #parent.setStyle("vertical-align", "middle")
        parent.setStyle("display", "inline-block")

        resetButtonHTML = (
            "<div style=\"display:inline-block\"><a href=\"javascript:var radio_buttons = document.getElementsByName('" + name + "'); "
                "for(var i = 0; i < radio_buttons.length; i++){"
                    "radio_buttons[i].checked = false;"
                "}"
            "\" style=\"display:inline-block; position:relative; top: 0px; padding-left:20px; text-decoration: none;\">Reset</a></div>")


        htmlResult = parser.getFormattedHTML(indent="\n    ")


        finalHTMLResult = "<br>" + htmlResult + resetButtonHTML


        return finalHTMLResult
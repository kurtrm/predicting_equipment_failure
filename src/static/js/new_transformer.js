"use strict";
(function(window, document) {
    $(".results").hide()


    let get_form_inputs = function() {
        let veg = $("input:checked");
        let age = $("input#Age").val();
        var inputs = {}
        for (let i = 0; i < veg.length; i++) {
            if (i <= 4) {
            inputs[veg[i].name] = veg[i].value;
            } else {        
            inputs[veg[i].id] = veg[i].value;
            };
        };
        inputs["Age"] = age;
        return inputs;
    }

    let send_form_inputs = function(inputs) {
        $.ajax({
            url: '/transformer_prediction',
            contentType: "application/json; charset=utf-8",
            type: 'POST',
            success: function(data) {
                display_prediction(data);
            },
            data: JSON.stringify(inputs)
        });
    };

    let display_prediction = function(data) {
        $(".results").show()
        $("span#probability").html(data.probability + "%")
        $("span#threshold").html(data.threshold + "%")
        if (data.probability < data.threshold) {
            $("span#probability").addClass("text-danger")
            var assess = "There is a " + data.probability + "% probability that this transformer will not incur additional costs." +
                         " Additionally, based on the selected threshold of " + data.threshold + "%, " + 
                         "it is recommended that an <b>enhanced preventive maintenance schedule</b> be applied to this unit.";
        } else {
            $("span#probability").addClass("text-success")
            var assess = "There is a " + data.probability + "% probability that this transformer will not incur additional costs." +
                         " Additionally, based on the selected threshold of " + data.threshold + "%, " + 
                         "it is recommended that this unit maintain a <b>normal preventive maintenance schedule</b>.";
        }
        $("span#assessment").html(assess)
    };

    $("button#send").click(function() {
        let inputs = get_form_inputs();
        if (inputs["Age"] === "" || isNaN(inputs["Age"]) || inputs["Age"] < 0) {
            $(".invalid-tooltip").show();
            return
        } else {
            $(".invalid-tooltip").hide();
        };
        send_form_inputs(inputs);
    });
})(window, document);

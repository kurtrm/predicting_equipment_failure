"use strict";

let get_form_inputs = function() {
    let veg = $("input:checked");
    let age = $("input#Age").val();
    var inputs = {}
    for (let i = 0; i < veg.length; i++) {
        if (i <= 4) {
        inputs[veg[i].name] = veg[i].value;
        } else {        
        inputs[veg[i].id] = veg[i].value;
        }
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

$("button#send").click(function() {
    let inputs = get_form_inputs();
    send_form_inputs(inputs);
});

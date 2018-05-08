"use strict";
// Be sure to make some jQuery substitutions where applicable
let preventionSlider = document.getElementById("preventionValues");
let failureSlider = document.getElementById("failureValues")
let preventionOutput = document.getElementById("prevention");
let failureOutput = document.getElementById("failure");
let totalOutput = document.getElementById("total");

preventionOutput.innerHTML = preventionSlider.value;
failureOutput.innerHTML = failureSlider.value;
totalOutput.innerHTML = parseInt(preventionSlider.value) + parseInt(failureSlider.value);

preventionSlider.oninput =  function() {
    preventionOutput.innerHTML = this.value;
    totalOutput.innerHTML = parseInt(preventionOutput.innerHTML) + parseInt(failureOutput.innerHTML);
}

failureSlider.oninput = function() {
    failureOutput.innerHTML = this.value;
    totalOutput.innerHTML = parseInt(this.value) + parseInt(preventionOutput.innerHTML);
}
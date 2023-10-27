function addQuestion() {
    var questionContainer = document.getElementById("added-questions");

    // Create a new question container
    var questionDiv = document.createElement("div");
    questionDiv.className = "question";

    var label1 = document.createElement("label");
    label1.innerHTML = "Activity:";
    label1.style.display = "block"; // Display the label as a block element
    //label1.style.marginBottom = "5px"; // Add some bottom margin
    label1.style.marginLeft="20px";
    label1.style.width = "34%";
    questionDiv.appendChild(label1); // Append the label to the questionDiv

    // Create dropdown input field 1
    var dropdownInput1 = document.createElement("select");
    dropdownInput1.innerHTML = 
    "<option value='select1'>Select Activity</option><option value='Option 1'>Option 1</option><option value='Option 2'>Option 2</option><option value='Option 3'>Option 3</option>";
    dropdownInput1.style.marginBottom = "10px"; // Add CSS styling
    dropdownInput1.style.width = "95%"; // Set width
    
    questionDiv.appendChild(dropdownInput1);
    
    var label2 = document.createElement("label");
    label2.innerHTML = "Skippable:";
    label2.style.display = "block"; // Display the label as a block element
    //label2.style.marginBottom = "5px"; // Add some bottom margin
    label2.style.width="34%";
    label2.style.marginLeft="20px";
    questionDiv.appendChild(label2); // Append the label to the questionDiv
    // Create dropdown input field 2
    var dropdownInput2 = document.createElement("select");
    dropdownInput2.innerHTML = "<option value='option2'>Skippable</option><option value='Option 1'>Option 1</option><option value='Option 2'>Option 2</option><option value='Option 3'>Option 3</option>";
    dropdownInput2.style.marginBottom = "10px"; // Add CSS styling
    dropdownInput2.style.width = "95%"; // Set width
    questionDiv.appendChild(dropdownInput2);


    // Create remove button
    var removeButton = document.createElement("button");
    removeButton.className = "btn btn-danger"; // Use Bootstrap's "danger" button style
    removeButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" class="bi bi-dash-circle-fill" viewBox="0 0 16 16">' +
      '<path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/>' +
      '</svg> Remove'; // SVG icon code for "dash-circle-fill"
    removeButton.addEventListener("click", function() {
      questionDiv.remove();
      questionCounter--;
      checkQuestionLimit();
    });
    questionDiv.appendChild(removeButton);

var table = document.createElement("table");
table.style.width = "100%"; // Set the table width to 100% to fill the available space

// Create the first row
var row1 = table.insertRow();
var cell1 = row1.insertCell();
cell1.appendChild(label1);
var cell2 = row1.insertCell();
cell2.appendChild(label2);


// Create the second row
var row2 = table.insertRow();
var cell3 = row2.insertCell();
cell3.style.width = "50%"; // Adjust the width of the cells as desired
cell3.appendChild(dropdownInput1);
var cell4 = row2.insertCell();
cell4.style.width = "50%"; // Adjust the width of the cells as desired
cell4.appendChild(dropdownInput2);
var cell5 = row2.insertCell(); // Add a cell for the remove button
cell5.appendChild(removeButton);

// Append the table to the questionDiv
questionDiv.appendChild(table);

var label3 = document.createElement("label");
    label3.innerHTML = "Question 1:";
    label3.style.display = "block"; // Display the label as a block element
    //label1.style.marginBottom = "5px"; // Add some bottom margin
    label3.style.marginLeft="20px";
    label3.style.width = "34%";
    questionDiv.appendChild(label3); // Append the label to the questionDiv

// Create skippable dropdown input field
var skippableDropdownInput = document.createElement("select");
skippableDropdownInput.innerHTML = "<option value='option3'>Select Activity</option><option value='Option 1'>Option 1</option><option value='Option 2'>Option 2</option><option value='Option 3'>Option 3</option>";
skippableDropdownInput.style.width = "95%"; // Set width
questionDiv.appendChild(skippableDropdownInput);

// Append the question container to the added-questions container
questionContainer.appendChild(questionDiv);
}
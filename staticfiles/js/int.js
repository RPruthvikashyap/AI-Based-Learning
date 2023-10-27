var episodeCount = 1;

function openPopup() {
  var popupOverlay = document.getElementById("popupOverlay");
  popupOverlay.style.display = "flex";
}

function openForm() {
  var formOverlay = document.getElementById("formOverlay");
  formOverlay.style.display = "flex";
}

function openActivityForm() {
  var activityFormOverlay = document.getElementById("activityFormOverlay");
  activityFormOverlay.style.display = "flex";
}

function addButtonClick() {
  var radio1 = document.getElementById("radio1");
  var radio2 = document.getElementById("radio2");

  if (radio1.checked) {
    openForm();
    var activityFormOverlay = document.getElementById("activityFormOverlay");
    activityFormOverlay.style.display = "none";
  } else if (radio2.checked) {
    openActivityForm();
    var formOverlay = document.getElementById("formOverlay");
    formOverlay.style.display = "none";
  }
}

function closePopup() {
  var popupOverlay = document.getElementById("popupOverlay");
  popupOverlay.style.display = "none";
  var activityFormOverlay = document.getElementById("activityFormOverlay");
  activityFormOverlay.style.display = "none";
  var formOverlay = document.getElementById("formOverlay");
  formOverlay.style.display = "none";
}

function closeopenform() {
  var formOverlay = document.getElementById("formOverlay");
  formOverlay.style.display = "none";
}

function closeActivityForm() {
  var activityFormOverlay = document.getElementById("activityFormOverlay");
  activityFormOverlay.style.display = "none";
}

function addNewEpisode() {
  var containers = document.querySelectorAll(".container1");
  var containerCount = containers.length;

  var newContainer = document.createElement("div");
  newContainer.className = "container1";
  newContainer.innerHTML = `
    <div>
      <h2>Episode ${containerCount + 1}</h2>
    </div>
    <button class="addbtn" onclick="openPopup()">  
      <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" fill="url(#gradient)" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#A20CA0" />
            <stop offset="30%" stop-color="#A00DA1" />
            <stop offset="100%" stop-color="#6020AF" />
          </linearGradient>
        </defs>
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z" />
      </svg>
    </button>`;

  if (containerCount === 0) {
    var nextButton = document.querySelector(".next");
    nextButton.parentNode.insertBefore(newContainer, nextButton);
  } else {
    var inserted = false;
    for (var i = 0; i < containerCount; i++) {
      var currentContainer = containers[i];
      var currentEpisode = parseInt(currentContainer.querySelector("h2").textContent.match(/\d+/)[0]);

      if (containerCount + 1 < currentEpisode) {
        currentContainer.parentNode.insertBefore(newContainer, currentContainer);
        inserted = true;
        break;
      }
    }

    if (!inserted) {
      var nextButton = document.querySelector(".next");
      nextButton.parentNode.insertBefore(newContainer, nextButton);
    }
  }
}

function showLoader() {
  var loaderContainer = document.getElementById("loaderContainer");
  if (loaderContainer) {
    loaderContainer.style.display = "flex";
  }
}

function hideLoader() {
  var loaderContainer = document.getElementById("loaderContainer");
  if (loaderContainer) {
    loaderContainer.style.display = "none";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  var generateScriptForm = document.getElementById("generateScriptForm");
  var csrfToken = "{{ csrf_token }}";

  generateScriptForm.addEventListener("submit", function (event) {
    event.preventDefault();
    showLoader();

    var formData = new FormData(generateScriptForm);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/generate_script/", true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        hideLoader(); 
        var response = JSON.parse(xhr.responseText);
        if (response.message) {
          alert(response.message);
          var formOverlay = document.getElementById("formOverlay");
          formOverlay.style.display = "none";

          window.location.reload();
        } else {
          alert(response.error);
        }
      }
    };

    xhr.send(formData);
  });
});
function editScript(title, generatedScript, scriptId, quiz) {
  console.log("Script ID: ", scriptId);
  var activityFormOverlay = document.getElementById("activityFormOverlay");
  activityFormOverlay.querySelector(".text.ele").value = title;
  activityFormOverlay.querySelector("textarea").value = generatedScript;
  activityFormOverlay.querySelector("input[name=scriptId]").value = scriptId;
  activityFormOverlay.querySelector("textarea[placeholder='Quiz']").value = quiz;
  activityFormOverlay.style.display = "flex";
}

function saveEditedScript() {
  var activityFormOverlay = document.getElementById("activityFormOverlay");
  var title = activityFormOverlay.querySelector(".text.ele").value;
  var generatedScript = activityFormOverlay.querySelector("textarea").value;
  var scriptId = activityFormOverlay.querySelector("input[name=scriptId]").value;
  var quizContent = activityFormOverlay.querySelector("textarea[placeholder='Quiz']").value;

  if (!scriptId) {
    alert("Invalid script ID. Please try again.");
    return;
  }

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/edit_script/" + scriptId + "/", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}"); 

  var formData = "generated_script=" + encodeURIComponent(generatedScript);
  formData += "&quiz=" + encodeURIComponent(quizContent);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        if (response.message) {
          alert(response.message);
          closeActivityForm();
          window.location.reload();
        } else {
          alert(response.error);
        }
      } else {
        alert("Failed to save the edited script. Please try again.");
      }
    }
  };

  xhr.send(formData);
}

function deleteScript(scriptId) {
  var confirmDelete = confirm("Are you sure you want to delete this script?");

  if (!confirmDelete) {
  }
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/delete_script/" + scriptId + "/", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        if (response.message) {
          alert(response.message);
          window.location.reload();
        } else {
          alert(response.error);
        }
      } else {
        alert("Failed to delete the script. Please try again.");
      }
    }
  };

  xhr.send();
}

function generateQuiz() {
  var activityFormOverlay = document.getElementById("activityFormOverlay");
  if (!activityFormOverlay) {
    alert("Activity form overlay not found. Please try again.");
    return;
  }
  var scriptId = activityFormOverlay.querySelector("input[name=scriptId]").value;
  var title = activityFormOverlay.querySelector(".text.ele").value;
  var generatedScript = activityFormOverlay.querySelector("textarea").value;

  if (!title || !generatedScript) {
    alert("Please enter title and generated script before generating the quiz.");
    return;
  }

  showLoader();

  var csrfToken = getCSRFToken();
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/generate_quiz/", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);

  var formData = "script_id=" + scriptId + "&title=" + encodeURIComponent(title) + "&generated_script=" + encodeURIComponent(generatedScript);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      hideLoader();

      if (xhr.status === 200) {
        try {
          var response = JSON.parse(xhr.responseText);
          console.log("Response:", response);

          if (response.quiz) {
            var quizTextarea = activityFormOverlay.querySelector("textarea[placeholder='Quiz']");
            if (quizTextarea) {
              quizTextarea.value = response.quiz;
              alert("Quiz generated successfully!");
              window.location.reload();
            } else {
              alert("Quiz textarea not found. Please try again.");
            }
          } else {
            alert("Invalid quiz data received from the server.");
          }
        } catch (error) {
          console.error("Error parsing the response:", error);
          alert("Failed to parse the response from the server. Please try again.");
        }
      } else {
        alert("Failed to fetch the quiz. Please try again.");
      }
    }
  };

  xhr.send(formData);
}

function getCSRFToken() {
  var csrfToken = null;
  var cookies = document.cookie.split(";");

  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i].trim();

    if (cookie.startsWith("csrftoken=")) {
      csrfToken = cookie.substring("csrftoken=".length, cookie.length);
      break;
    }
  }

  return csrfToken;
}

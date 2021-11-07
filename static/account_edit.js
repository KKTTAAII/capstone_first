const editBtn = document.getElementById("editBtn");

editBtn.addEventListener("click", function () {
  let formDiv = document.getElementById("update-user");
  if (formDiv.style.display === "block") {
    formDiv.style.display = "none";
  } else {
    formDiv.style.display = "block";
    editBtn.style.display = "none";
  }
});

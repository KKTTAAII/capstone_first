const editBtn = document.getElementById("editBtn");

editBtn.addEventListener("click", function () {
  let formDiv = document.getElementById("update-user");
  formDiv.classList.toggle("hide");
  editBtn.classList.toggle("hide");
});

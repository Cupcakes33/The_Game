
const menuSwitch = () => {
  $(".login-form-wrapper").addClass("switch");
  $(".register-form-wrapper").addClass("switch");
};

const buttonActive = () => {
  if ($("#id").val() !== "" && $("#pw").val() !== "") {
    $("#signIn").addClass("active");
  } else {
    $("#signIn").removeClass("active");
  }
};

$(".login-form").submit((e) => {
  e.preventDefault();
  const userData = {
    id: $("#id").val(),
    pw: $("#pw").val(),
  };
  console.log(userData);
});

$(".register-form").submit((e) => {
  e.preventDefault();
});

// Form switch

$("#id").on("input", () => {
  buttonActive();
});
$("#pw").on("input", () => {
  buttonActive();
});
$(".login-form-signup-link").click(() => {
  menuSwitch();
});

$("#regist_id").focusout((e) => {
  if ($(e.target).val() === "") {
    $(".currectID").removeClass("active");
    $(".invalidID").removeClass("active");
  } else if ($(e.target).val() === "0") {
    $(".currectID").removeClass("active");
    $(".invalidID").addClass("active");
  } else {
    console.log($("#regist_id").val());
    $(".invalidID").removeClass("active");
    $(".currectID").addClass("active");
  }
});

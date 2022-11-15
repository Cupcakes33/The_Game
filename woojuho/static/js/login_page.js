
const menuSwitch = () => {
  $(".login-form-wrapper").addClass("switch");
  $(".register-form-wrapper").addClass("switch");
};

const buttonActive = () => {
  if ($("#id").val() !== "" && $("#pw").val() !== "") {
    $("#signIn").attr('disabled',false)
    $("#signIn").addClass("active");

  } else {
    $("#signIn").attr('disabled',true)
    $("#signIn").removeClass("active");
  }
};

$(".login-form").submit((e) => {
  e.preventDefault();

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

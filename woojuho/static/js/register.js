const registAccount = () => {
  $.ajax({
    type: "POST",
    url: "/api/register",
    data: {
      regist_id: $('#regist_id').val(),
      regist_id: $('#regist_pw').val(),
      regist_nickname: $('#regist_nickname').val(),
    },
    success: (res) => {
      console.log(res)
    }
  });
};

$('.register-form').submit((e)=>{
  e.preventDefault();
  registAccount()
  alert('Account Create !!!')
  window.location.reload();
})
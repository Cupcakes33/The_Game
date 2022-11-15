// const registAccount = () => {
//   $.ajax({
//     type: "POST",
//     url: "/api/register",
//     data: {
//       id_give: $('#regist_id').val(),
//       pw_give: $('#regist_pw').val(),
//       nickname_give: $('#regist_nickname').val(),
//     },
//     success: (res) => {
//       console.log(res)
//     }
//   });
// };
//
// $('.register-form').submit((e)=>{
//   e.preventDefault();
//   registAccount()
//   alert('Account Create !!!')
//   window.location.reload();
// })
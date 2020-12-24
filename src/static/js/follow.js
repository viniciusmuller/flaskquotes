const followButton = document.querySelector(".follow-btn");
const profileOwnerFollowers = document.querySelector("#prof-owner-followers");

if (followButton) {
  let callback =
    followButton.innerHTML == "Follow" ? followEvent : unfollowEvent;
  followButton.addEventListener("click", callback);
}

// TODO improve code and remove current user
// from followers modal after unfollow
async function followEvent(_event) {
  let usertag = this.getAttribute("usertag");

  let response = await fetch(`/follow/${usertag}`);
  let body = await response.json();
  // Redirecting user to login page if the API
  // returns that he is not authenticated
  if (!body.authenticated) return redirectLogin();

  this.innerHTML = "Unfollow";
  profileOwnerFollowers.innerText = Number(profileOwnerFollowers.innerText) + 1;

  // Swapping callbacks
  this.removeEventListener("click", followEvent);
  this.addEventListener("click", unfollowEvent);
}

async function unfollowEvent(_event) {
  let usertag = this.getAttribute("usertag");

  let response = await fetch(`/unfollow/${usertag}`);
  let body = await response.json();
  if (!body.authenticated) return redirectLogin();

  this.innerHTML = "Follow";
  profileOwnerFollowers.innerHTML -= 1;

  // Swapping callbacks
  this.removeEventListener("click", unfollowEvent);
  this.addEventListener("click", followEvent);
}

function redirectLogin() {
  window.location.href = "/login";
}

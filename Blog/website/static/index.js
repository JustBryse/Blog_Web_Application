// this function sends requests to the views.like_post function and recieves like data in response
function like(postId)
{
  const likeCount = document.getElementById(`likes-count-${postId}`); // get like count span element
  const likeButton = document.getElementById(`like-button-${postId}`); // get like button icon element

  // send a request to the views.like_post() function. views.like_post() will send back a json object as a response
  fetch(`/like-post/${postId}`, {method:"POST"})
  .then((res) => res.json())
  .then((data) => {
    console.log(data);
    // always update the like count that views.like_post() sends to this function
    likeCount.innerHTML = data["likes"];
    // depending on whether views.like_post() tells us if the post is liked, select the like icon's class accordingly
    if(data["liked"] === true)
    {
      likeButton.className = "fas fa-thumbs-up";
    }
    else
    {
      likeButton.className = "far fa-thumbs-up";
    }

  }).catch((e) => alert("Could not like post.")); // this happens if the request to views.like_post() failed
}

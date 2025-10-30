// async function importImages() {
//   const folderId = document.getElementById("folderId").value;
//   const res = await fetch(`http://127.0.0.1:8000/import/${folderId}`, { method: "POST" });
//   const data = await res.json();
//   showImages(data);
// }

// async function showImages(images) {
//   const gallery = document.getElementById("gallery");
//   gallery.innerHTML = "";
//   images.forEach(img => {
//     const i = document.createElement("img");
//     i.src = img.cloudinary_url;
//     i.width = 200;
//     gallery.appendChild(i);
//   });
// }

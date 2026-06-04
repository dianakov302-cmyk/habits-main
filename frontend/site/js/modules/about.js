export function initAbout() {
  const aboutVideo = document.getElementById('aboutVideo');

  if (!aboutVideo) return;

  aboutVideo.addEventListener('click', () => {
    window.open('https://www.youtube.com/@anaida13', '_blank');
  });
}

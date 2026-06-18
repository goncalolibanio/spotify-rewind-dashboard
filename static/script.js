const toggle = document.querySelector('.nav-toggle');
const menu = document.querySelector('[data-menu]');

if (toggle && menu) {
  toggle.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

const reveals = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

reveals.forEach((element) => revealObserver.observe(element));

// --- FLASK AJAX & PLOTLY INTEGRATION ---
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const uploadStatus = document.getElementById('uploadStatus');
const dashboardWrapper = document.getElementById('dashboard-wrapper');

function updateDashboardUI(data) {
  // Update Hero Preview Data
  const formattedMins = parseInt(data.kpis.total_min).toLocaleString();
  const formattedSongs = parseInt(data.kpis.unique_songs).toLocaleString();
  
  document.getElementById('hero-metric-min').textContent = formattedMins;
  document.getElementById('hero-metric-songs').textContent = formattedSongs;
  document.getElementById('hero-metric-artist').textContent = data.kpis.top_artist;
  
  document.getElementById('hero-window-min').textContent = formattedMins + " min";
  document.getElementById('hero-window-days').textContent = Math.round(data.kpis.total_min / 60 / 24) + " days listening to music";
  
  document.getElementById('hero-window-artist').textContent = data.kpis.top_artist;
  document.getElementById('hero-window-artist-skip').textContent = data.kpis.skip_percentage + "% skip rate";
  document.getElementById('hero-window-profile').textContent = data.kpis.listener_profile;
  document.getElementById('hero-window-day').textContent = data.kpis.binge_day.split(',')[0];
  document.getElementById('hero-window-ghost').textContent = data.kpis.ghost_songs;
  
  document.getElementById('hero-floating-artist').textContent = data.kpis.top_artist;
  
  // Update KPI Cards
  document.getElementById('kpi-minutes').textContent = formattedMins;
  document.getElementById('kpi-top-artist').textContent = data.kpis.top_artist;
  document.getElementById('kpi-unique-songs').textContent = formattedSongs;
  document.getElementById('kpi-skip').textContent = data.kpis.skip_percentage + '%';
  
  // Update Insights Text
  document.getElementById('insight-binge').textContent = `Your biggest day was ${data.kpis.binge_day} with ${data.kpis.binge_hours} hours. Top artist: ${data.kpis.binge_artist}.`;
  document.getElementById('insight-ghost').textContent = `You listened to ${data.kpis.ghost_songs} songs between 00:00 and 05:00.`;
  document.getElementById('insight-profile').textContent = `Your algorithm profile is: ${data.kpis.listener_profile}.`;

  // Show Dashboard Wrapper with Fade
  dashboardWrapper.style.display = 'block';
  // Trigger reflow
  void dashboardWrapper.offsetWidth;
  dashboardWrapper.style.opacity = '1';

  // Render Plotly Charts
  Plotly.newPlot('plotly-eras', data.charts.eras.data, data.charts.eras.layout, {responsive: true});
  Plotly.newPlot('plotly-general', data.charts.general.data, data.charts.general.layout, {responsive: true});
  Plotly.newPlot('plotly-rhythm-heat', data.charts.rhythm_heat.data, data.charts.rhythm_heat.layout, {responsive: true});
  Plotly.newPlot('plotly-rhythm-end', data.charts.rhythm_end.data, data.charts.rhythm_end.layout, {responsive: true});
}

// Check for existing session data on page load
window.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('/api/session-data');
    if (response.ok) {
      const data = await response.json();
      if (data && data.success) {
        updateDashboardUI(data);
      }
    }
  } catch (err) {
    console.error('Failed to restore session cache:', err);
  }
});

if (uploadBtn && fileInput) {
  uploadBtn.addEventListener('click', (e) => {
    e.preventDefault();
    fileInput.click();
  });

  fileInput.addEventListener('change', async () => {
    const files = fileInput.files;
    if (files.length === 0) return;

    // Loading State
    const originalBtnHTML = uploadBtn.innerHTML;
    uploadBtn.innerHTML = `
      Processing...
      <svg viewBox="0 0 24 24" aria-hidden="true" style="animation: spin 1s linear infinite;"><path d="M12 4V2A10 10 0 0 0 2 12h2a8 8 0 0 1 8-8z" /></svg>
    `;
    uploadBtn.style.opacity = '0.8';
    uploadBtn.style.pointerEvents = 'none';
    uploadStatus.textContent = '';
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to process data');
      }

      // Restore button
      uploadBtn.innerHTML = originalBtnHTML;
      uploadBtn.style.opacity = '1';
      uploadBtn.style.pointerEvents = 'auto';

      uploadStatus.textContent = 'Success!';
      uploadStatus.style.color = 'var(--green-2)';
      
      updateDashboardUI(data);

      setTimeout(() => uploadStatus.textContent = '', 4000);
      
      // Scroll to dashboard
      document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });
      
    } catch (err) {
      uploadBtn.innerHTML = originalBtnHTML;
      uploadBtn.style.opacity = '1';
      uploadBtn.style.pointerEvents = 'auto';
      uploadStatus.textContent = 'Error: ' + err.message;
      uploadStatus.style.color = '#ff5f57';
    }
  });
}

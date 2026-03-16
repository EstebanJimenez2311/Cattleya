/**
 * data/charts.js — Configuraciones centralizadas de todos los gráficos
 *
 * ¿Cómo usar?
 * 1. Cada clave del objeto CHARTS corresponde al `chart-id` de un <cat-chart>
 * 2. Reemplaza los arrays `data` con los valores reales de tu análisis en Python
 * 3. Exporta los resultados del notebook como JSON y úsalos aquí directamente
 *
 * ¿Cómo exportar desde Python?
 *   import json
 *   datos = df['tipo_violencia'].value_counts().to_dict()
 *   with open('data/resultados.json', 'w') as f:
 *       json.dump(datos, f)
 */

window.CHARTS = {

  // ─────────────────────────────────────────
  // PÁGINA: analisis.html
  // ─────────────────────────────────────────

  'chart-evolucion': {
    type: 'line',
    data: {
      labels: ['2018','2019','2020','2021','2022','2023'],
      // TODO: Reemplazar con datos reales del dataset
      datasets: [{
        label: 'Casos reportados',
        data: [145000, 158000, 132000, 167000, 178000, 182000],
        borderColor: '#9D2D6A',
        backgroundColor: 'rgba(157,45,106,0.08)',
        borderWidth: 3,
        pointBackgroundColor: '#9D2D6A',
        pointRadius: 6,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { font: { family: 'DM Sans' } } },
        x: { grid: { display: false }, ticks: { font: { family: 'DM Sans' } } }
      }
    }
  },

  'chart-departamentos': {
    type: 'bar',
    data: {
      // TODO: Reemplazar con top 10 departamentos reales
      labels: ['Bogotá','Antioquia','Valle','Cundinamarca','Santander',
               'Atlántico','Bolívar','Nariño','Córdoba','Meta'],
      datasets: [{
        label: 'Casos',
        data: [42000, 31000, 24000, 18000, 14000, 12000, 10000, 8500, 7200, 6800],
        backgroundColor: '#9D2D6A',
        borderRadius: 6,
        hoverBackgroundColor: '#F28C28'
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false, indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { font: { family: 'DM Sans' } } },
        y: { grid: { display: false }, ticks: { font: { family: 'DM Sans', size: 11 } } }
      }
    }
  },

  'chart-edad': {
    type: 'bar',
    data: {
      // TODO: Reemplazar con grupos de edad reales del dataset
      labels: ['0-12','13-17','18-24','25-34','35-44','45-54','55-64','65+'],
      datasets: [{
        label: 'Casos',
        data: [3200, 8900, 22000, 38000, 31000, 18000, 9200, 4100],
        backgroundColor: ['#9D2D6A','#822157','#F28C28','#FDEEE9','#d4700a','#c44d8e','#f0a854','#6b1a47'],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { font: { family: 'DM Sans' } } },
        x: { grid: { display: false }, ticks: { font: { family: 'DM Sans' } } }
      }
    }
  },

  'chart-tipo': {
    type: 'doughnut',
    data: {
      // TODO: Reemplazar con distribución real por tipo de violencia
      labels: ['Física','Psicológica','Sexual','Económica','Negligencia'],
      datasets: [{
        data: [38, 29, 18, 11, 4],
        backgroundColor: ['#9D2D6A','#822157','#F28C28','#c44d8e','#d4700a'],
        borderWidth: 0, hoverOffset: 8
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { font: { family: 'DM Sans', size: 12 }, padding: 14 }
        }
      }
    }
  },

  'chart-meses': {
    type: 'bar',
    data: {
      labels: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
      // TODO: Reemplazar con promedio mensual real
      datasets: [{
        label: 'Promedio de casos',
        data: [14200,13100,15800,14900,16200,15400,14800,15100,14300,15900,16800,17200],
        backgroundColor: (ctx) => [10, 11].includes(ctx.dataIndex) ? '#F28C28' : '#9D2D6A',
        borderRadius: 8
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { font: { family: 'DM Sans' } } },
        x: { grid: { display: false }, ticks: { font: { family: 'DM Sans' } } }
      }
    }
  },

  // ─────────────────────────────────────────
  // PÁGINA: index.html (preview)
  // ─────────────────────────────────────────

  'chart-home': {
    type: 'doughnut',
    data: {
      labels: ['Física','Psicológica','Sexual','Económica','Negligencia'],
      datasets: [{
        data: [38, 29, 18, 11, 4],
        backgroundColor: ['#9D2D6A','#822157','#F28C28','#FDEEE9','#d4700a'],
        borderWidth: 0, hoverOffset: 8
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { font: { family: 'DM Sans', size: 13 }, color: '#333333', padding: 16 }
        },
        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw}%` } }
      }
    }
  },

  // ─────────────────────────────────────────
  // PÁGINA: tendencias.html
  // Agregar aquí los gráficos de ML e inferencial
  // ─────────────────────────────────────────

  // 'chart-correlacion': { ... },
  // 'chart-confusion':   { ... },
  // 'chart-roc':         { ... },

};

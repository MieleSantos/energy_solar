document.addEventListener('DOMContentLoaded', () => {
    fetchPlants();

    const form = document.getElementById('plant-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const plantData = {
            name: document.getElementById('name').value,
            location: document.getElementById('location').value,
            capacity_kw: parseFloat(document.getElementById('capacity_kw').value),
            status: document.getElementById('status').value
        };

        try {
            const response = await fetch('/api/plants', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(plantData)
            });

            if (response.ok) {
                form.reset();
                fetchPlants();
            } else {
                alert('Erro ao cadastrar usina.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Erro de conexão.');
        }
    });
});

async function fetchPlants() {
    try {
        const response = await fetch('/api/plants');
        const plants = await response.json();
        
        updateDashboard(plants);
        renderTable(plants);
    } catch (error) {
        console.error('Error fetching plants:', error);
    }
}

function updateDashboard(plants) {
    document.getElementById('total-plants').textContent = plants.length;
    
    const totalCapacity = plants.reduce((sum, plant) => sum + plant.capacity_kw, 0);
    // Formata o número (ex: 12500 -> 12,500.00)
    const formattedCapacity = new Intl.NumberFormat('pt-BR', { style: 'decimal', maximumFractionDigits: 2 }).format(totalCapacity);
    document.getElementById('total-capacity').textContent = `${formattedCapacity} kW`;
}

function getStatusClass(status) {
    switch (status) {
        case 'Ativa': return 'status-ativa';
        case 'Manutenção': return 'status-manutencao';
        case 'Inativa': return 'status-inativa';
        case 'Em Construção': return 'status-construcao';
        default: return 'status-ativa';
    }
}

function renderTable(plants) {
    const tbody = document.getElementById('plants-tbody');
    tbody.innerHTML = '';

    if (plants.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: var(--text-muted);">Nenhuma usina cadastrada.</td></tr>`;
        return;
    }

    plants.forEach((plant, index) => {
        const tr = document.createElement('tr');
        tr.style.animationDelay = `${index * 0.05}s`;
        
        const capacityFormatted = new Intl.NumberFormat('pt-BR', { style: 'decimal', maximumFractionDigits: 2 }).format(plant.capacity_kw);

        tr.innerHTML = `
            <td><strong>${plant.name}</strong></td>
            <td>${plant.location}</td>
            <td>${capacityFormatted} kW</td>
            <td><span class="status-badge ${getStatusClass(plant.status)}">${plant.status}</span></td>
            <td>
                <button class="btn-icon btn-delete" onclick="deletePlant(${plant.id})" title="Excluir">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function deletePlant(id) {
    if (!confirm('Tem certeza que deseja excluir esta usina?')) return;

    try {
        const response = await fetch(`/api/plants/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            fetchPlants();
        } else {
            alert('Erro ao excluir usina.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

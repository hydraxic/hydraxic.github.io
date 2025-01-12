const items = [];

fetch('items-list/equipment.json')
    .then(response => response.json())
    .then(item => {
        console.log('Loaded items:', item);
        item.forEach(item => items.push(item.name));
    })
    .catch(error => console.error('Error loading items:', error));

// perform fuzzy search

function searchItems() {
    const input = document.getElementById('search-input').value.toLowerCase();
    const resultsContainer = document.getElementById('results');
    const materialsResultsContainer = document.getElementById('material-results');
    const template = document.getElementById('equipment-table-template');

    resultsContainer.innerHTML = '';

    if (input == '') { return; }

    const matches = items.filter(item => item.toLowerCase().includes(input));

    matches.forEach(match => {
        const button = document.createElement('button');
        button.className = 'result-button';
        button.textContent = match;

        button.onclick = () => {
            if (materialsResultsContainer.innerHTML.indexOf(match) == -1) {
                const clone = template.content.cloneNode(true);
                const materialsTable = clone.querySelector('.crafting-materials');
                const upgradesTable = clone.querySelector('.crafting-materials-upgrade');

                const detailsTable = clone.querySelector('#details-table');
                const detailsTableUpgrade = clone.querySelector('#details-table-upgrade');
                
                equipmentName = clone.querySelector('.item-name');

                if (!materialsTable) { console.error('No crafting materials table found'); return; } else { console.log('Found crafting materials table'); }

                fetch('items-list/equipment.json')
                    .then(response => response.json())
                    .then(item => {
                        item.forEach(item => {
                            console.log(item);
                            console.log(item.name);
                            console.log(match);
                            if (item.name == match) {
                                console.log('Found match');

                                equipmentName.textContent = item.name + ' ';
                                var img = document.createElement('img');
                                img.src = 'images/weapon-icons/' + item.type + '.png';
                                img.style.height = '1.2em';
                                equipmentName.appendChild(img);

                                item['materials-forge'].forEach(material => {
                                    const materialRow = document.createElement('tr');

                                    const materialName = document.createElement('th');
                                    const materialQuantity = document.createElement('th');

                                    materialName.textContent = material.name;
                                    materialQuantity.textContent = material.quantity;

                                    fetch('items-list/materials.json')
                                        .then(response => response.json())
                                        .then(material => {
                                            material.forEach(material => {
                                                if (material.name == materialName.textContent) {
                                                    material.source.forEach(sources => {
                                                        const detailsRow = document.createElement('tr');
                                                        sources.forEach(source => {
                                                            const tempCell = document.createElement('th');
                                                            tempCell.textContent = source;
                                                            detailsRow.appendChild(tempCell);
                                                        })
                                                        detailsTable.appendChild(detailsRow);
                                                    })
                                                }
                                            })
                                        })
                                        .catch(error => console.error('Error loading items:', error));

                                    materialRow.appendChild(materialName);
                                    materialRow.appendChild(materialQuantity);
                                    materialsTable.appendChild(materialRow);
                                })

                                item['materials-upgrade'].forEach(material => {
                                    const materialRow = document.createElement('tr');

                                    const materialName = document.createElement('th');
                                    const materialQuantity = document.createElement('th');

                                    materialName.textContent = material.name;
                                    materialQuantity.textContent = material.quantity;

                                    fetch('items-list/materials.json')
                                        .then(response => response.json())
                                        .then(material => {
                                            material.forEach(material => {
                                                if (material.name == materialName.textContent) {
                                                    material.source.forEach(sources => {
                                                        const detailsRow = document.createElement('tr');
                                                        sources.forEach(source => {
                                                            const tempCell = document.createElement('th');
                                                            tempCell.textContent = source;
                                                            detailsRow.appendChild(tempCell);
                                                        })
                                                        detailsTableUpgrade.appendChild(detailsRow);
                                                    })
                                                }
                                            })
                                        })
                                        .catch(error => console.error('Error loading items:', error));

                                    materialRow.appendChild(materialName);
                                    materialRow.appendChild(materialQuantity);
                                    upgradesTable.appendChild(materialRow);
                                })
                            }
                        })
                    })
                    .catch(error => console.error('Error loading items:', error));

                materialsResultsContainer.appendChild(clone);
            }
        }

        resultsContainer.appendChild(button);
    });
}

function closeCard(button) {
    const card = button.parentElement;
    card.remove();
}
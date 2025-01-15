const items = [];

fetch('items-list/equipment.json')
    .then(response => response.json())
    .then(item => {
        console.log('Loaded items:', item);
        item.forEach(item => items.push(item.name));
    })
    .catch(error => console.error('Error loading items:', error));

function addMaterialSourceDetails(materialName)
{
    if (materialName.parentElement.parentElement.parentElement.className == 'crafting-materials') { // forging
        const clone = materialName.parentElement.parentElement.parentElement.parentElement // item info div
        const detailsTable = clone.querySelector('#details-table');
        const detailsDropsTable = clone.querySelector('#details-drops-table');
        
        const title = clone.querySelector('#details-box-title');
        title.textContent = materialName.textContent;

        detailsTable.innerHTML = '';
        detailsDropsTable.innerHTML = '';

        fetch('items-list/materials.json')
            .then(response => response.json())
            .then(material => {
                material.forEach(material => {
                    if (material.name == materialName.textContent) {
                        material.source.forEach(sources => {
                            const detailsRow = document.createElement('tr');
                            const detailsDropsRow = document.createElement('tr');
                            sources.forEach(source => {
                                if (/^\d+%$/.test(source)) { // percentage chance, add to a different sortable table.
                                    const tempCell = document.createElement('th');
                                    tempCell.textContent = source;
                                    detailsDropsRow.appendChild(tempCell);
                                } else if (/^x\d+$/.test(source)) { // how many will drop, add to different sortable table, same as percentage
                                    const tempCell = document.createElement('th');
                                    tempCell.textContent = source;
                                    detailsDropsRow.appendChild(tempCell);
                                } else {
                                    const tempCell = document.createElement('th');
                                    tempCell.textContent = source;
                                    detailsRow.appendChild(tempCell);
                                }
                            })
                            detailsTable.appendChild(detailsRow);
                            detailsDropsTable.appendChild(detailsDropsRow);
                        })
                    }
                })
            })
            .catch(error => console.error('Error loading items:', error));
    }
    else if (materialName.parentElement.parentElement.parentElement.className == 'crafting-materials-upgrade') { // upgrading
        const clone = materialName.parentElement.parentElement.parentElement.parentElement // item info div
        const detailsTableUpgrade = clone.querySelector('#details-table-upgrade');
        const detailsDropsTableUpgrade = clone.querySelector('#details-drops-table-upgrade');

        const title = clone.querySelector('#details-box-title-upgrade');
        title.textContent = materialName.textContent;

        detailsTableUpgrade.innerHTML = '';
        detailsDropsTableUpgrade.innerHTML = '';

        fetch('items-list/materials.json')
            .then(response => response.json())
            .then(material => {
                material.forEach(material => {
                    if (material.name == materialName.textContent) {
                        material.source.forEach(sources => {
                            const detailsRow = document.createElement('tr');
                            const detailsDropsRow = document.createElement('tr');
                            sources.forEach(source => {
                                if (/^\d+%$/.test(source)) { // percentage chance, add to a different sortable table.
                                    const tempCell = document.createElement('th');
                                    tempCell.textContent = source;
                                    detailsDropsRow.appendChild(tempCell);
                                } else if (/^x\d+$/.test(source)) { // how many will drop, add to different sortable table, same as percentage
                                    const tempCell = document.createElement('th');
                                    tempCell.textContent = source;
                                    detailsDropsRow.appendChild(tempCell);
                                } else {
                                    const tempCell = document.createElement('th');
                                    tempCell.textContent = source;
                                    detailsRow.appendChild(tempCell);
                                }
                            })
                            detailsTableUpgrade.appendChild(detailsRow);
                            detailsDropsTableUpgrade.appendChild(detailsDropsRow);
                        })
                    }
                })
            })
            .catch(error => console.error('Error loading items:', error));
    }
}

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
            if (!Array.from(materialsResultsContainer.querySelectorAll('h2')).some(node => node.textContent === match)) {
                console.log('Adding item:', match);
                const clone = template.content.cloneNode(true);
                const materialsTable = clone.querySelector('.crafting-materials');
                const upgradesTable = clone.querySelector('.crafting-materials-upgrade');
                const detailsTitle = clone.querySelector('#details-box-title');
                const detailsUpgradeTitle = clone.querySelector('#details-box-title-upgrade');
                
                equipmentName = clone.querySelector('.item-name');

                if (!materialsTable) { console.error('No crafting materials table found'); return; } else { console.log('Found crafting materials table'); }

                fetch('items-list/equipment.json')
                    .then(response => response.json())
                    .then(item => {
                        item.forEach(item => {
                            if (item.name == match) {
                                console.log('Found match');

                                equipmentName.textContent = item.name + ' ';
                                var img = document.createElement('img');
                                img.src = 'images/weapon-icons/' + item.type + '.png';
                                img.style.height = '1.2em';
                                equipmentName.appendChild(img);

                                if (item['materials-forge'].length == 0) {
                                    detailsTitle.textContent = 'Weapon cannot be forged';
                                }

                                if (item['materials-upgrade'].length == 0) {
                                    detailsUpgradeTitle.textContent = 'Weapon cannot be upgraded';
                                }

                                item['materials-forge'].forEach(material => {
                                    const materialRow = document.createElement('tr');

                                    const materialName = document.createElement('th');
                                    const materialNameButton = document.createElement('button');
                                    const materialQuantity = document.createElement('th');

                                    materialNameButton.textContent = material.name;
                                    materialNameButton.onclick = function() { addMaterialSourceDetails(materialNameButton); };
                                    materialNameButton.className = 'material-button';
                                    materialQuantity.textContent = material.quantity;

                                    materialName.appendChild(materialNameButton);
                                    materialRow.appendChild(materialName);
                                    materialRow.appendChild(materialQuantity);
                                    materialsTable.appendChild(materialRow);
                                })

                                item['materials-upgrade'].forEach(material => {
                                    const materialRow = document.createElement('tr');

                                    const materialName = document.createElement('th');
                                    const materialNameButton = document.createElement('button');
                                    const materialQuantity = document.createElement('th');

                                    materialNameButton.textContent = material.name;
                                    materialNameButton.onclick = function() { addMaterialSourceDetails(materialNameButton); };
                                    materialNameButton.className = 'material-button';
                                    materialQuantity.textContent = material.quantity;

                                    materialName.appendChild(materialNameButton);
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
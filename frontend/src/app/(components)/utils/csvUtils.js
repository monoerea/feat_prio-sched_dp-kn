export const parseCsv = (text) => {
    const lines = text.split('\n');
    const headers = lines[0].split(',');
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim() !== '') {
            const values = lines[i].split(',');
            const row = {};

            for (let j = 0; j < headers.length; j++) {
                row[headers[j]] = values[j];
            }

            data.push(row);
        }
    }

    return data;
};
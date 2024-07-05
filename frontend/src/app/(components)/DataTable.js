import React from 'react';

const DataTable = ({ data, displayRowCount }) => {
    return (
        <div className="overflow-y-auto max-h-96 bg-slate-800 rounded-lg pt-3">
            <table className="border-collapse border border-slate-500 text-sm">
                <thead>
                    <tr className="bg-slate-700">
                        {Object.keys(data[0]).map((header, index) => (
                            <th key={index} className="border border-gray-400 px-3 py-1">
                                {header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.slice(0, displayRowCount).map((row, rowIndex) => (
                        <tr key={rowIndex} className="border border-gray-400">
                            {Object.values(row).map((value, cellIndex) => (
                                <td key={cellIndex} className="border border-gray-400 px-3 py-1">
                                    {value}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
            {data.length > displayRowCount && (
                <p className="mt-2 text-sm text-gray-600">
                    Showing {displayRowCount} out of {data.length} rows.
                </p>
            )}
        </div>
    );
};

export default DataTable;

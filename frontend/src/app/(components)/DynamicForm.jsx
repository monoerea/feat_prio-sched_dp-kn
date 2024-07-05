import React from 'react';
import AbstractInput from './AbstractInput';

const DynamicForm = ({ fields, handleFormDataChange }) => {
    // Get unique group numbers
    const groupNumbers = [...new Set(fields.map(field => field.group))];

    // Function to render fields by group number
    const renderFieldsByGroup = (groupNumber) => {
        // Filter fields based on the group number
        const fieldsInGroup = fields.filter(field => field.group === groupNumber);

        console.log('fieldsInGroup',fieldsInGroup.length);
        // Set a maximum number of columns

        // Determine the number of columns based on the number of fields in the group
        const columns = Math.min(fieldsInGroup.length, 3);
                let gridClass;
                // Define the grid class based on the number of columns
                if (columns === 1) {
                    gridClass = 'md:w-full';
                } else if (columns === 2) {
                    gridClass = 'md:grid-cols-2';
                } else if (columns === 3) {
                    gridClass = 'md:grid-cols-3';
                }

        // Render each field in the group
        return fieldsInGroup.map((field, idx) => (
            <div key={idx} className={`mb-4 ${gridClass} md:gap-4 `}>
                <label
                    className="block text-gray-300 font-bold mb-2 truncate hover:whitespace-normal max-w-2xl"
                    htmlFor={field.name}
                    title={field.name} // Tooltip with full name
                    style={{ wordWrap: 'break-word' }}
                >
                    <div className="min-h-12 flex items-center">{field.name}</div>
                </label>
                <AbstractInput
                    type={'number'}
                    id={field.id}
                    placeholder={field.placeholder}
                    onChange={handleFormDataChange}
                />
            </div>
        ));
    };


    return (
        <div className='grid grid-cols-1'>
            {/* Render fields for each group */}
            {groupNumbers.map((groupNumber, idx) => {
                // Determine the number of columns for this group
                const fieldsInGroup = fields.filter(field => field.group === groupNumber);
                const columns = fieldsInGroup.length;

                // Define the grid class based on the number of columns
                let gridClass;
                if (columns === 4) {
                    gridClass = 'md:grid-cols-4';
                } else if (columns === 2) {
                    gridClass = 'md:grid-cols-2';
                } else if (columns === 3) {
                    gridClass = 'md:grid-cols-3';
                } else {
                    gridClass = 'md:grid-cols-1';
                }
                return (
                    <div key={idx} className={`grid ${gridClass} md:gap-4 mb-4 xs:grid-cols-1`}>
                        {renderFieldsByGroup(groupNumber)}
                    </div>
                );
            })}
        </div>
    );
};

export default DynamicForm;

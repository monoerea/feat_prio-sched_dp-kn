import React, { useState } from 'react';

const AbstractInput = ({ type, id, value, placeholder, validate, onChange}) => {
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const val = event.target.value;
    // Validate the input value if the validate function is provided
    if (validate && !validate(val)) {
      setError('Invalid input');
    } else {
      setError('');
    }
    onChange(id, val); // Pass id and value to the onChange handler
  };

  return (
    <div className='mt-2'>
      <input
        step=".01"
        type={type}
        id={id}
        required
        name={id}
        value={value} // Ensure that the value prop is passed to the input
        autoComplete={id}
        onChange={onChange} // Use handleChange function for onChange event
        placeholder={placeholder}
        className={' w-full py-1.5 px-3 border border-gray-500 text-slate-400 leading-tight block rounded-md focus:ring-2 focus:ring-inset focus:ring-sky-600 sm:text-sm sm:leading-6 bg-slate-500'}
      />
      {error && (
        <p className='mt-2 text-sm text-red-400'>{error}</p>
      )}
    </div>
  );
};

export default AbstractInput;

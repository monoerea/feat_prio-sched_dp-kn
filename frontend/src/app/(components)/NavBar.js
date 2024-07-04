// Navbar.jsx
import React from 'react';
import Link from 'next/link'; // Import Link from next/link for client-side navigation
import { navItems } from './utils/constants';

const NavBar = () => {
    return (
        <nav className=' ml-3 flex flex-row justify-between '>
            <div className='pr-10 flex flex-row'>
                <div className='p-3'>
                    logo
                </div>
                <ul className=' flex flex-row'>
                    {navItems.map((item, index) => (
                        <li className={' p-3 hover:text-blue-500 ease-in-out duration-300 transform motion-safe:hover:scale-110 '} key={index}>
                            <Link className='visited:text-purple-600' href={item.path}>{item.name}</Link>
                        </li>
                    ))}
                </ul>
            </div>
            <div className='p-3'>
                feat
            </div>
            
        </nav>
    );
};

export default NavBar;

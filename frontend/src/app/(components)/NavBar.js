// Navbar.jsx
import React from 'react';
import Link from 'next/link'; // Import Link from next/link for client-side navigation
import { navItems } from './utils/constants';
import Image from 'next/image';
const NavBar = () => {
    return (
        <nav className='fixed flex flex-row justify-between bg-slate-800 w-full'>
            <div className='pr-10 flex flex-row'>
                <Image className='p-3' src = {'feat-white.svg'} width={100} height={100}/>
                <ul className=' flex flex-row'>
                    {navItems.map((item, index) => (
                        <li className={' p-3 hover:text-blue-500 ease-in-out duration-300 transform motion-safe:hover:scale-110 '} key={index}>
                            <Link className='visited:text-white' href={item.path}>{item.name}</Link>
                        </li>
                    ))}
                </ul>
            </div>
        </nav>
    );
};

export default NavBar;

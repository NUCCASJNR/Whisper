import { FC, ReactNode } from 'react';
// import { Link } from 'react-router-dom';
// import { Logo } from '../components';
// import { HeaderLinkPropType } from '../interfaces';

// const HeaderLink: FC<HeaderLinkPropType> = ({ to, text }) => {
//   return (
//     <Link to={to} className="hover:bg-gray-700 p-2 rounded">
//       {text}
//     </Link>
//   );
// };

const Header: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <header className="border-secondary border-b-2 max-h-[15%] bg-white m-0 text-text text-xl p-8 flex items-center">
      {children}
    </header>
  );
};

export default Header;

// // UsersContext.tsx
// import { createContext, FC, useContext, useState, useEffect } from 'react';
// import {
//   ActiveUser,
//   UsersContextType,
//   UsersProviderProps,
// } from '../interfaces';
// import data from '../services/data.json'; // Assuming dummy data is stored here

// const UsersContext = createContext<UsersContextType | undefined>(undefined);

// export const UsersProvider: FC<UsersProviderProps> = ({ children }) => {
//   const [activeUsers, setActiveUsers] = useState<ActiveUser[]>([]);

//   // Load initial user data from a JSON file (or this could come from an API)
//   useEffect(() => {
//     setUsers(data.users); // `data.users` contains an array of users
//   }, []);

//   return (
//     <UsersContext.Provider value={{ users, setUser }}>
//       {children}
//     </UsersContext.Provider>
//   );
// };

// // Custom hook to use the UsersContext
// export const useUsers = () => {
//   const context = useContext(UsersContext);
//   if (!context) {
//     throw new Error('useUsers must be used within a UsersProvider');
//   }
//   return context;
// };

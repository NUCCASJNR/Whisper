import { FC, useState } from 'react';
import { useApi } from '../contexts';
import { useNavigate } from 'react-router-dom';
import { Header, SingleLayout } from '../layouts';
import { FaUserCircle, FaEye, FaEyeSlash, FaEdit } from 'react-icons/fa';

const ProfilePage: FC = () => {
  const { logout, user, updateProfile } = useApi();
  const navigate = useNavigate();

  const [isEditing, setIsEditing] = useState(false);
  const [username, setUsername] = useState(user?.username || '');
  const [userBio, setUserBio] = useState(user?.bio || '');
  const [readyToChat, setReadyToChat] = useState(user?.readyToChat || false);
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  // Store original values when editing starts
  const [initialUsername, setInitialUsername] = useState(username);
  const [initialBio, setInitialBio] = useState(userBio);
  const [initialReadyToChat, setInitialReadyToChat] = useState(readyToChat);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleToggleReady = () => {
    const newReadyStatus = !readyToChat;
    setReadyToChat(newReadyStatus);
    if (user) {
      updateProfile({ ...user, readyToChat: newReadyStatus });
    }
  };

  const handleProfileUpdate = async () => {
    try {
      updateProfile({
        bio: userBio,
        username,
        ready_to_chat: readyToChat,
        password,
      });
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile');
    }
  };

  const startEditing = () => {
    setInitialUsername(username);
    setInitialBio(userBio);
    setInitialReadyToChat(readyToChat);
    setIsEditing(true);
  };

  const cancelEditing = () => {
    setUsername(initialUsername);
    setUserBio(initialBio);
    setReadyToChat(initialReadyToChat);
    setIsEditing(false);
  };

  return (
    <SingleLayout>
      <Header>
        <h1 className="text-xl sm:text-2xl font-semibold text-primary">
          Welcome, {user?.username}
        </h1>
      </Header>
      <div className="h-full px-4 sm:px-0">
        <div className="flex justify-center items-center h-full">
          <div className="bg-white dark:bg-gray-100 text-text p-6 sm:p-8 shadow-lg rounded-md w-full max-w-xs sm:max-w-md">
            <div className="flex flex-col items-center mb-6">
              <div className="relative w-24 h-24 rounded-full overflow-hidden">
                <FaUserCircle className="w-full h-full text-gray-300" />
              </div>

              {!isEditing && (
                <span className="text-lg sm:text-xl font-semibold mt-2">
                  {username}
                  <button
                    onClick={startEditing}
                    className="text-gray-500 text-sm sm:text-base ml-2 p-1 rounded hover:bg-gray-600 hover:text-white transition"
                  >
                    <FaEdit />
                  </button>
                </span>
              )}
            </div>

            {isEditing && (
              <div className="mb-4">
                <label className="block text-sm sm:text-base font-medium">
                  Username:
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value.trim())}
                  className="border border-gray-300 rounded p-1 w-full"
                />
              </div>
            )}

            <div className="mb-4">
              <label className="block text-sm sm:text-base font-medium">
                Bio:
              </label>
              {isEditing ? (
                <textarea
                  value={userBio}
                  onChange={(e) => setUserBio(e.target.value.trim())}
                  className="border border-gray-300 rounded p-1 w-full"
                />
              ) : (
                <p>{userBio || 'No bio available'}</p>
              )}
            </div>

            <div className="flex items-center mb-4">
              <label className="mr-2 text-sm sm:text-base">
                Ready to Chat:
              </label>
              <input
                type="checkbox"
                checked={readyToChat}
                onChange={handleToggleReady}
                className="toggle-checkbox"
                disabled={!isEditing}
              />
            </div>

            {isEditing && (
              <div className="mb-4">
                <label className="block text-sm sm:text-base font-medium">
                  Password:
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="border border-gray-300 rounded p-1 w-full"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500"
                  >
                    {showPassword ? <FaEyeSlash /> : <FaEye />}
                  </button>
                </div>
              </div>
            )}

            <div className="flex gap-4 mt-4 justify-end">
              {isEditing ? (
                <>
                  <button
                    onClick={handleProfileUpdate}
                    className="bg-primary dark:bg-primary-dark text-white text-sm sm:text-base p-2 sm:p-3 rounded hover:bg-opacity-80 transition"
                  >
                    Save Changes
                  </button>
                  <button
                    onClick={cancelEditing}
                    className="bg-red-500 text-white text-sm sm:text-base p-2 sm:p-3 rounded hover:bg-red-600 transition"
                  >
                    Cancel
                  </button>
                </>
              ) : (
                <button
                  onClick={handleLogout}
                  className="bg-red-500 text-white text-sm sm:text-base p-2 sm:p-3 rounded hover:bg-red-600 transition"
                >
                  Logout
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </SingleLayout>
  );
};

export default ProfilePage;

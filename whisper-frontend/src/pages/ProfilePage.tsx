import { FC, useState } from 'react';
import { useAuth } from '../contexts';
import { useNavigate } from 'react-router-dom';
import { ChangePasswordModal } from '../components'; // Modal component
import { Header, SingleLayout } from '../layouts';
import { FaUserCircle } from 'react-icons/fa'; // Icon for avatar

const ProfilePage: FC = () => {
  const { logout, user, updateUserStatus } = useAuth();
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [readyToChat, setReadyToChat] = useState(user?.readyToChat || false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleToggleReady = () => {
    const newReadyStatus = !readyToChat;
    setReadyToChat(newReadyStatus);
    if (user) {
      updateUserStatus({ ...user, readyToChat: newReadyStatus });
    }
  };

  const handlePasswordChange = (newPassword: string) => {
    console.log('Password updated to:', newPassword);
    setIsModalOpen(false); // Close modal after password change
  };

  return (
    <SingleLayout>
      <Header>
        <h1 className="text-xl sm:text-2xl font-semibold">Your Profile</h1>
      </Header>
      <div className="h-full px-4 sm:px-0">
        <div className="flex justify-center items-center h-full">
          <div className="bg-secondary text-text p-6 sm:p-8 shadow-lg rounded-md w-full max-w-xs sm:max-w-md">
            <div className="flex flex-col items-center mb-6">
              <div className="relative w-24 h-24 rounded-full overflow-hidden">
                {/* Avatar Placeholder */}
                <FaUserCircle className="w-full h-full text-gray-300" />
              </div>
              <h2 className="text-lg sm:text-xl font-semibold mt-2">
                {user?.username}
              </h2>
            </div>

            <p className="mb-2 text-sm sm:text-base">
              <strong>Public Key:</strong> {user?.publicKey}
            </p>

            {/* Toggle Ready to Chat */}
            <div className="flex items-center mb-4">
              <label className="mr-2 text-sm sm:text-base">
                Ready to Chat:
              </label>
              <input
                type="checkbox"
                checked={readyToChat}
                onChange={handleToggleReady}
                className="toggle-checkbox"
              />
            </div>

            {/* Buttons */}
            <div className="flex gap-4 mt-4">
              <button
                onClick={() => setIsModalOpen(true)}
                className="bg-blue-500 text-white text-sm sm:text-base p-2 sm:p-3 rounded hover:bg-blue-600 transition"
              >
                Change Password
              </button>
              <button
                onClick={handleLogout}
                className="bg-red-500 text-white text-sm sm:text-base p-2 sm:p-3 rounded hover:bg-red-600 transition"
              >
                Logout
              </button>
            </div>
          </div>

          {/* Modal for Password Change */}
          {isModalOpen && (
            <ChangePasswordModal
              onClose={() => setIsModalOpen(false)}
              onSubmit={handlePasswordChange}
            />
          )}
        </div>
      </div>
    </SingleLayout>
  );
};

export default ProfilePage;

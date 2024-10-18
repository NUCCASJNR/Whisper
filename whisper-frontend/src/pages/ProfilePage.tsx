import { FC, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import Modal from '../components/Auth/ChangePasswordModal'; // We'll create this Modal component later.

const ProfilePage: FC = () => {
  const { logout, user, updateUserStatus } = useAuth(); // Add updateUserStatus for "Ready to Chat"
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false); // Modal state
  const [readyToChat, setReadyToChat] = useState(user?.readyToChat || false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleToggleReady = () => {
    setReadyToChat(!readyToChat);
    if (user) {
      updateUserStatus({ ...user, readyToChat: !readyToChat }); // Update user "Ready to Chat" status
    }
  };

  const handlePasswordChange = (newPassword: string) => {
    // Add your logic for updating the password here.
    console.log('Password updated to:', newPassword);
    setIsModalOpen(false); // Close modal after password change
  };

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Profile</h1>
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <div className="bg-white p-8 shadow-lg rounded-md">
          <p className="mb-2">
            <strong>Username:</strong> {user?.username}
          </p>
          <p className="mb-2">
            <strong>Public Key:</strong> {user?.publicKey}
          </p>

          {/* Toggle Ready to Chat */}
          <div className="flex items-center mb-4">
            <label className="mr-2">Ready to Chat:</label>
            <input
              type="checkbox"
              checked={readyToChat}
              onChange={handleToggleReady}
              className="toggle-checkbox"
            />
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => setIsModalOpen(true)} // Open modal on button click
              className="bg-blue-500 text-white p-2 rounded"
            >
              Change Password
            </button>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white p-2 rounded"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Modal for Password Change */}
        {isModalOpen && (
          <Modal
            onClose={() => setIsModalOpen(false)}
            onSubmit={handlePasswordChange}
          />
        )}
      </div>
    </div>
  );
};

export default ProfilePage;

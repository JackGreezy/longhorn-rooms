// components/ProfileImage.tsx




import Image from 'next/image';


const ProfileImageWyatt = () => {
 return (
   <div className="profile-image-container">
     <Image
       src="/DopeWyatt.JPG" // Path relative to the public folder
       alt="Profile Image"
       width={300} // Specify the width (adjust as needed)
       height={300} // Specify the height (adjust as needed)
       layout="fixed" // Ensures it scales based on the container size
       className="rounded-lg" // Optional styling
     />
   </div>
 );
};


export default ProfileImageWyatt;
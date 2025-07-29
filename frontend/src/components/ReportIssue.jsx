import React, { useState } from 'react';
import { FiMapPin, FiX } from 'react-icons/fi';
import { toast } from 'react-toastify';

const ReportIssue = () => {
  // State for the form inputs
  const [issueType, setIssueType] = useState('Illegal Dumping / Litter');
  const [location, setLocation] = useState('');
  const [comments, setComments] = useState('');
  const [uploadedPhoto, setUploadedPhoto] = useState(null);
  const [photoPreview, setPhotoPreview] = useState('');
  
  // State for UI feedback
  const [isLocating, setIsLocating] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleDetectLocation = () => {
    if (!navigator.geolocation) {
      toast.error('Geolocation is not supported by your browser.');
      return;
    }

    toast.promise(
      new Promise(async (resolve, reject) => {
        setIsLocating(true);
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const { latitude, longitude } = position.coords;
            try {
              const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
              if (!response.ok) throw new Error('Failed to fetch address.');
              const data = await response.json();
              
              if (data && data.display_name) {
                setLocation(data.display_name);
                resolve(data.display_name);
              } else {
                const coords = `Lat: ${latitude.toFixed(5)}, Lon: ${longitude.toFixed(5)}`;
                setLocation(coords);
                resolve(coords);
              }
            } catch (error) {
              const coords = `Lat: ${latitude.toFixed(5)}, Lon: ${longitude.toFixed(5)}`;
              setLocation(coords);
              reject('Could not find address. Using coordinates.');
            } finally {
              setIsLocating(false);
            }
          },
          (error) => {
            setIsLocating(false);
            reject('Unable to retrieve location. Please check permissions.');
          }
        );
      }),
      {
        pending: 'Detecting your location...',
        success: 'Location detected!',
        error: {
          render({data}){
            return data;
          }
        }
      }
    );
  };

  const handlePhotoUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) { // 10MB size limit
        toast.error("File is too large. Please select a file smaller than 10MB.");
        return;
      }
      setUploadedPhoto(file);
      setPhotoPreview(URL.createObjectURL(file));
      toast.success("Photo uploaded successfully!");
    }
  };

  const handleRemovePhoto = () => {
    setUploadedPhoto(null);
    setPhotoPreview('');
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setIsSubmitting(true);

    // Simulate an API call
    setTimeout(() => {
      console.log({ issueType, location, comments, uploadedPhoto });
      toast.success("Report submitted successfully! Thank you.");
      
      // Reset form fields
      setIssueType('Illegal Dumping / Litter');
      setLocation('');
      setComments('');
      handleRemovePhoto();
      setIsSubmitting(false);
    }, 1500);
  };

  return (
    <section className="container mx-auto px-6 py-16">
      <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Report an Issue</h2>
        <p className="text-gray-600 mb-8">
          Help keep our community clean. Use this form to report litter or other waste-related issues.
        </p>
        <form className="space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="issue-type" className="block text-sm font-medium text-gray-700">Type of Issue</label>
            <select
              id="issue-type"
              name="issue-type"
              value={issueType}
              onChange={(e) => setIssueType(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm rounded-md"
            >
              <option>Illegal Dumping / Litter</option>
              <option>Overflowing Bin</option>
              <option>Damaged Public Bin</option>
              <option>Other</option>
            </select>
          </div>

          <div>
            <div className="flex justify-between items-center">
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">Location Description</label>
              <button
                type="button"
                onClick={handleDetectLocation}
                disabled={isLocating}
                className="flex items-center text-sm font-medium text-teal-600 hover:text-teal-800 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <FiMapPin className="mr-1 h-4 w-4" />
                {isLocating ? 'Locating...' : 'Detect Current Location'}
              </button>
            </div>
            <input
              type="text"
              name="location"
              id="location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g., Near the park entrance on Main St."
              required
              className="mt-1 focus:ring-teal-500 focus:border-teal-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label htmlFor="comments" className="block text-sm font-medium text-gray-700">Additional Details</label>
            <textarea
              id="comments"
              name="comments"
              rows={4}
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              className="mt-1 shadow-sm focus:ring-teal-500 focus:border-teal-500 block w-full sm:text-sm border border-gray-300 rounded-md"
              placeholder="Describe the issue in more detail..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Upload a Photo (Optional)</label>
            <div className="mt-1">
              {photoPreview ? (
                <div className="relative group">
                  <img src={photoPreview} alt="Issue preview" className="w-full h-auto rounded-md" />
                  <button
                    type="button"
                    onClick={handleRemovePhoto}
                    className="absolute top-2 right-2 bg-black bg-opacity-50 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                    aria-label="Remove photo"
                  >
                    <FiX className="h-5 w-5" />
                  </button>
                </div>
              ) : (
                <div className="flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div className="space-y-1 text-center">
                    <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                      <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    <div className="flex text-sm text-gray-600">
                      <label htmlFor="file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-teal-600 hover:text-teal-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-teal-500">
                        <span>Upload a file</span>
                        <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handlePhotoUpload} accept="image/png, image/jpeg, image/gif" />
                      </label>
                      <p className="pl-1">or drag and drop</p>
                    </div>
                    <p className="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:bg-teal-400 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Report'}
            </button>
          </div>
        </form>
      </div>
    </section>
  );
};

export default ReportIssue;



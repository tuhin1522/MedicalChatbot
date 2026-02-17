import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

const VerifyEmail: React.FC = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const statusParam = searchParams.get('status');
  const messageParam = searchParams.get('message');
  
  console.log('URL Parameters:', { token, statusParam, messageParam });
  
  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>(
    statusParam === 'success' ? 'success' : statusParam === 'error' ? 'error' : 'verifying'
  );
  const [message, setMessage] = useState(
    messageParam ? decodeURIComponent(messageParam.replace(/\+/g, ' ')) : 'Verifying your email...'
  );

  useEffect(() => {
    console.log('useEffect triggered with:', { token, statusParam });
    
    // If we already have status from redirect, don't verify again
    if (statusParam) {
      console.log('Status already present, skipping API call');
      return;
    }

    // If no status but have token, verify directly via API
    if (token && !statusParam) {
      console.log('No status param, calling API to verify');
      verifyDirectly(token);
    } else if (!token && !statusParam) {
      console.log('No token and no status');
      setStatus('error');
      setMessage('No verification token provided.');
    }
  }, [token, statusParam]);

  const verifyDirectly = async (token: string) => {
    try {
      console.log('Verifying token:', token);
      
      // Call backend verification endpoint - backend will return JSON for fetch calls
      const response = await fetch(`http://localhost:8000/auth/verify/${token}`, {
        headers: {
          'Accept': 'application/json'
        }
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);
      
      // Check if response is ok before trying to parse JSON
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        setStatus('error');
        setMessage('Verification failed. Please try again or contact support.');
        return;
      }

      const data = await response.json();
      console.log('Response data:', data);
      
      if (data.status === 'success') {
        setStatus('success');
        setMessage(data.message || 'Email verified successfully! You can now login.');
      } else {
        setStatus('error');
        setMessage(data.message || 'Verification failed. Please try again.');
      }
      
    } catch (error) {
      console.error('Verification error:', error);
      setStatus('error');
      setMessage('An error occurred during verification. Please check the console and try again.');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <Card className="w-full max-w-md mx-4">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            {status === 'verifying' && <Loader2 className="h-16 w-16 text-blue-500 animate-spin" />}
            {status === 'success' && <CheckCircle2 className="h-16 w-16 text-green-500" />}
            {status === 'error' && <XCircle className="h-16 w-16 text-red-500" />}
          </div>
          <CardTitle className="text-2xl">
            {status === 'verifying' && 'Verifying Email'}
            {status === 'success' && 'Email Verified!'}
            {status === 'error' && 'Verification Failed'}
          </CardTitle>
        </CardHeader>
        <CardContent className="text-center">
          <CardDescription className="text-base">
            {message}
          </CardDescription>
        </CardContent>
        {status !== 'verifying' && (
          <CardFooter className="flex justify-center">
            <Link to="/">
              <Button size="lg">
                {status === 'success' ? 'Go to Dashboard' : 'Return to Home'}
              </Button>
            </Link>
          </CardFooter>
        )}
      </Card>
    </div>
  );
};

export default VerifyEmail;

import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/services/api";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!token) {
        toast.error("Invalid reset link.");
        navigate('/');
    }
  }, [token, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (newPassword !== confirmPassword) {
        toast.error("Passwords do not match");
        return;
    }

    if (newPassword.length < 6) {
        toast.error("Password must be at least 6 characters long");
        return;
    }

    setIsLoading(true);
    
    try {
      if (!token) {
        throw new Error("Invalid reset token");
      }

      const data = await api.resetPassword(token, newPassword);
      toast.success(data.message || "Password reset successfully. Please login.");
      
      // Navigate to home after short delay
      setTimeout(() => navigate('/'), 1500);
      
    } catch (err: any) {
      toast.error(err.message || "Failed to reset password");
    } finally {
      setIsLoading(false);
    }
  };

  if (!token) return null;

  return (
    <div className="flex h-screen items-center justify-center bg-muted/50 p-4">
        <Card className="w-full max-w-md">
            <CardHeader>
                <CardTitle>Reset Password</CardTitle>
                <CardDescription>Enter your new password below.</CardDescription>
            </CardHeader>
            <form onSubmit={handleSubmit}>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <label htmlFor="new-password" className="text-sm font-medium">New Password</label>
                        <Input 
                            id="new-password" 
                            type="password" 
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            required
                            placeholder="Enter new password"
                        />
                    </div>
                    <div className="space-y-2">
                        <label htmlFor="confirm-password" className="text-sm font-medium">Confirm Password</label>
                        <Input 
                            id="confirm-password" 
                            type="password" 
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                            placeholder="Confirm new password"
                        />
                    </div>
                </CardContent>
                <CardFooter>
                    <Button type="submit" className="w-full" disabled={isLoading}>
                         {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                         Reset Password
                    </Button>
                </CardFooter>
            </form>
        </Card>
    </div>
  );
}

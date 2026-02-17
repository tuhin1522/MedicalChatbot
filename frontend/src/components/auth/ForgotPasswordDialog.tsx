import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/services/api";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";

interface ForgotPasswordDialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  trigger?: React.ReactNode;
  onBackToLogin?: () => void;
}

export function ForgotPasswordDialog({ open, onOpenChange, trigger, onBackToLogin }: ForgotPasswordDialogProps) {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [internalOpen, setInternalOpen] = useState(false);

  const isControlled = open !== undefined;
  const show = isControlled ? open : internalOpen;
  const setShow = isControlled ? onOpenChange : setInternalOpen;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const data = await api.forgotPassword(email);
      toast.success(data.message || 'Password reset link sent to your email');
      
      // Clear form and close dialog
      setEmail('');
      if (setShow) setShow(false);
    } catch (err: any) {
      toast.error(err.message || "An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={show} onOpenChange={setShow}>
      {trigger && <DialogTrigger asChild>{trigger}</DialogTrigger>}
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Forgot Password</DialogTitle>
          <DialogDescription>
            Enter your email address and we'll send you a link to reset your password.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="grid gap-4 py-4">
          <div className="grid gap-2">
            <label htmlFor="reset-email" className="text-sm font-medium leading-none">
              Email
            </label>
            <Input
              id="reset-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="m@example.com"
              required
              disabled={isLoading}
            />
          </div>
          <DialogFooter className="flex flex-col sm:justify-between sm:flex-row gap-2">
            <div className="text-sm text-center sm:text-left mt-2 sm:mt-0">
               Remember your password?{" "}
               <button 
                type="button" 
                onClick={(e) => {
                  e.preventDefault();
                  if (setShow) setShow(false);
                  onBackToLogin?.();
                }}
                className="text-blue-500 hover:underline"
                disabled={isLoading}
               >
                 Login
               </button>
            </div>
            <Button type="submit" disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Send Reset Link
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

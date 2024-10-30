import React, { useEffect, useState } from "react";

import axios from "axios";

const url = "api/signup";
interface SingUpResData {
  result: boolean;
}
interface Props {
  onLogedIn: (user_name: string) => void;
}
const SignupForm = ({ onLogedIn }: Props) => {
  const [userName, setUserName] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(false);
  const [signUpResData, setSignUpRes] = useState<SingUpResData>({
    result: false,
  });
  const handleSubmit = () => {
    setIsLoading(true);
    const user = { user_name: userName };
    axios
      .post(url, user)
      .then((res) => {
        setSignUpRes(res.data);
        setIsLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setIsLoading(false);
      });
  };

  useEffect(() => {
    if (signUpResData.result) {
      onLogedIn(userName);
    }
  }, [signUpResData]);

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        handleSubmit();
      }}
    >
      <div className="mb-3">
        <label htmlFor="exampleInputEmail1" className="form-label">
          User Name
        </label>
        <input
          type="text"
          value={userName}
          onChange={(data) => setUserName(data.target.value)}
          className="form-control"
          id="exampleInputEmail1"
        />
        {error && <p className="text-danger">{error}</p>}
      </div>
      <button disabled={isLoading} type="submit" className="btn btn-primary">
        Sign Up
      </button>
    </form>
  );
};

export default SignupForm;

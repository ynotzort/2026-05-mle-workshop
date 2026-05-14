from datetime import date
from pathlib import Path
import tempfile

from duration_prediction.train import train


class TestTrain:
    def test_regression(self):
        # given
        with tempfile.TemporaryDirectory() as tmpdir:
            train_date = date(2022, 1, 1)
            val_date = date(2022, 2, 1)
            out_path = Path(tmpdir) / "model.bin"
        
            # when
            mse = train(train_date=train_date, val_date=val_date, out_path=out_path)

            # then 
            assert abs(8.189 - mse) < 0.01

    def test_model_file_gets_created(self):
        # given
        with tempfile.TemporaryDirectory() as tmpdir:
            train_date = date(2022, 1, 1)
            val_date = date(2022, 2, 1)
            out_path = Path(tmpdir) / "model.bin"
            
            assert not out_path.exists()
        
            # when
            train(train_date=train_date, val_date=val_date, out_path=out_path)

            # then 
            assert out_path.exists()

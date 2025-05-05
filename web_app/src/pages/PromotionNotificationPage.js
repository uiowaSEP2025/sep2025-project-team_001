import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  IconButton,
  Paper,
  Snackbar,
  Stack,
  TextField,
  Typography,
  Alert,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';

function PromotionNotificationPage() {
  const [promotions, setPromotions] = useState([]);
  const [newPromotion, setNewPromotion] = useState({ title: '', body: '' });
  const [editing, setEditing] = useState(null);
  const [confirmSendId, setConfirmSendId] = useState(null);
  const [flash, setFlash] = useState({
    open: false,
    message: '',
    severity: 'success',
  });

  const showFlash = (message, severity = 'success') => {
    setFlash({ open: true, message, severity });
  };

  const fetchPromotions = async () => {
    try {
      const res = await axios.get(
        `${process.env.REACT_APP_API_URL}/promotions/`,
      );
      setPromotions(res.data);
    } catch (err) {
      showFlash('Failed to load promotions.', 'error');
    }
  };

  useEffect(() => {
    fetchPromotions();
  }, []);

  const handleCreate = async () => {
    if (!newPromotion.title || !newPromotion.body) {
      return showFlash('Title and body are required', 'error');
    }

    try {
      await axios.post(
        `${process.env.REACT_APP_API_URL}/promotions/create/`,
        newPromotion,
      );
      setNewPromotion({ title: '', body: '' });
      fetchPromotions();
      showFlash('Promotion created!');
    } catch (err) {
      showFlash('Error creating promotion', 'error');
    }
  };

  const handleUpdate = async (promotionId, updated) => {
    try {
      await axios.patch(
        `${process.env.REACT_APP_API_URL}/promotions/${promotionId}/update/`,
        updated,
      );
      setEditing(null);
      fetchPromotions();
      showFlash('Promotion updated!');
    } catch (err) {
      showFlash('Error updating promotion', 'error');
    }
  };

  const handleDelete = async (promotionId) => {
    try {
      await axios.delete(
        `${process.env.REACT_APP_API_URL}/promotions/${promotionId}/delete/`,
      );
      fetchPromotions();
      showFlash('Promotion deleted!');
    } catch (err) {
      showFlash('Error deleting promotion', 'error');
    }
  };

  const handleSend = async (promotionId) => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_URL}/promotions/${promotionId}/send/`,
      );
      setConfirmSendId(null);
      fetchPromotions();
      showFlash('Promotion sent to all customers!');
    } catch (err) {
      showFlash('Error sending promotion', 'error');
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Promotions
      </Typography>

      <Paper elevation={3} sx={{ p: 2, mb: 4 }}>
        <Typography variant="h6">Create New Promotion</Typography>
        <Stack spacing={2} mt={2}>
          <TextField
            label="Title"
            value={newPromotion.title}
            onChange={(e) =>
              setNewPromotion({ ...newPromotion, title: e.target.value })
            }
          />
          <TextField
            label="Body"
            multiline
            rows={3}
            value={newPromotion.body}
            onChange={(e) =>
              setNewPromotion({ ...newPromotion, body: e.target.value })
            }
          />
          <Button variant="contained" onClick={handleCreate}>
            Create
          </Button>
        </Stack>
      </Paper>

      {promotions.length === 0 ? (
        <Typography>No promotions yet.</Typography>
      ) : (
        promotions.map((promo) => (
          <Paper key={promo.id} elevation={2} sx={{ p: 2, mb: 2 }}>
            {editing === promo.id ? (
              <Stack spacing={2}>
                <TextField
                  label="Title"
                  value={promo.title}
                  onChange={(e) =>
                    setPromotions((prev) =>
                      prev.map((p) =>
                        p.id === promo.id ? { ...p, title: e.target.value } : p,
                      ),
                    )
                  }
                />
                <TextField
                  label="Body"
                  multiline
                  rows={2}
                  value={promo.body}
                  onChange={(e) =>
                    setPromotions((prev) =>
                      prev.map((p) =>
                        p.id === promo.id ? { ...p, body: e.target.value } : p,
                      ),
                    )
                  }
                />
                <Stack direction="row" spacing={1}>
                  <Button
                    onClick={() => handleUpdate(promo.id, promo)}
                    variant="contained"
                  >
                    Save
                  </Button>
                  <Button onClick={() => setEditing(null)}>Cancel</Button>
                </Stack>
              </Stack>
            ) : (
              <Box>
                <Typography variant="h6">{promo.title}</Typography>
                <Typography>{promo.body}</Typography>
                <Stack direction="row" spacing={1} mt={1}>
                  <IconButton
                    color="primary"
                    onClick={() => setEditing(promo.id)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    color="error"
                    onClick={() => handleDelete(promo.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                  <IconButton
                    color="success"
                    onClick={() => setConfirmSendId(promo.id)}
                    disabled={promo.sent}
                  >
                    <SendIcon />
                  </IconButton>
                </Stack>
              </Box>
            )}
          </Paper>
        ))
      )}

      {/* Send confirmation dialog */}
      <Dialog open={!!confirmSendId} onClose={() => setConfirmSendId(null)}>
        <DialogTitle>Confirm Send</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to send this promotion to all customers using
            the Streamline app?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmSendId(null)}>No</Button>
          <Button variant="contained" onClick={() => handleSend(confirmSendId)}>
            Yes, Send
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={flash.open}
        autoHideDuration={4000}
        onClose={() => setFlash({ ...flash, open: false })}
      >
        <Alert severity={flash.severity} sx={{ width: '100%' }}>
          {flash.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default PromotionNotificationPage;

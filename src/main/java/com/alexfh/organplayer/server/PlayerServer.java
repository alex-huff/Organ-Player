package com.alexfh.organplayer.server;

import com.alexfh.organplayer.organ.Organ;

import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

public
class PlayerServer extends Thread
{

    @Override
    public
    void run()
    {
        try (ServerSocket serverSocket = new ServerSocket(18589))
        {
            while (true)
            {
                try (Socket socket = serverSocket.accept())
                {
                    this.handleClient(socket);
                }
                catch (IOException io)
                {
                    io.printStackTrace();
                }
            }
        }
        catch (IOException io)
        {
            io.printStackTrace();
        }
    }

    private
    void handleClient(Socket socket) throws IOException
    {
        InputStream socketInputStream = socket.getInputStream();
        int         message;
        while ((message = socketInputStream.read()) != -1)
        {
            boolean pressed = (message & 0x80) > 0;
            int     octave  = (message >> 4) & 0x7;
            int     note    = message & 0x0F;
            Organ.playNote(pressed, octave, note);
        }
    }

}
